import os
from datetime import date

from django.apps import apps
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _

from base.horilla_company_manager import HorillaCompanyManager
from employee.models import Employee
from horilla.models import HorillaModel, upload_path

STATUS = [
    ("requested", "Requested"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
]
FORMATS = [
    ("any", "Any"),
    ("pdf", "PDF"),
    ("txt", "TXT"),
    ("docx", "DOCX"),
    ("xlsx", "XLSX"),
    ("jpg", "JPG"),
    ("png", "PNG"),
    ("jpeg", "JPEG"),
]


def document_upload_path(instance, filename):
    """Store employee files below category/subcategory with a stable name."""
    ext = os.path.splitext(filename)[1].lower() or ".bin"
    employee = instance.employee_id
    employee_name = "dipendente"
    if employee:
        employee_name = slugify(
            f"{employee.employee_first_name or ''}{employee.employee_last_name or ''}"
        ) or employee_name
    category = slugify(instance.category.name) if instance.category else "senza-categoria"
    subcategory = slugify(instance.subcategory.name) if instance.subcategory else ""
    start = instance.start_date.strftime("%d%m%Y") if instance.start_date else "nodatainizio"
    folder = "/".join(part for part in ("documents", category, subcategory) if part)
    return f"{folder}/{employee_name}_{category}_{start}_{timezone.now():%d%m%Y}{ext}"


class DocumentCategory(HorillaModel):
    name = models.CharField(max_length=200, unique=True, verbose_name=_("Category"))

    class Meta:
        ordering = ["name"]
        verbose_name = _("Document Category")
        verbose_name_plural = _("Document Categories")

    def __str__(self):
        return self.name


class DocumentSubCategory(HorillaModel):
    name = models.CharField(max_length=200, verbose_name=_("Sub Category"))
    category = models.ForeignKey(
        DocumentCategory, on_delete=models.CASCADE, related_name="subcategories"
    )

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["name", "category"], name="unique_document_subcategory")]

    def __str__(self):
        return self.name


def document_create(instance):
    employees = instance.employee_id.all()
    for employee in employees:
        document = Document.objects.get_or_create(
            employee_id=employee,
            document_request_id=instance,
            defaults={"title": f"Upload {instance.title}"},
        )
        document[0].title = f"Upload {instance.title}"
        document[0].save()


class DocumentRequest(HorillaModel):
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    employee_id = models.ManyToManyField(Employee, verbose_name=_("Employees"))
    format = models.CharField(choices=FORMATS, max_length=10, verbose_name=_("Format"))
    max_size = models.IntegerField(
        blank=True, null=True, verbose_name=_("Max size (In MB)")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    objects = HorillaCompanyManager(
        related_company_field="employee_id__employee_work_info__company_id"
    )

    def get_edit_url(self):
        """
        Returns the edit url of the document request
        """

        return reverse_lazy("document-request-update", args=[self.pk])

    def get_delete_url(self):
        """
        Returns the delete url of the document request
        """

        return reverse_lazy("document-request-delete", args=[self.pk])

    class Meta:
        """
        Meta class to add additional options
        """

        verbose_name = _("Document Request")
        verbose_name_plural = _("Document Requests")

    def __str__(self):
        return self.title


class Maternita(HorillaModel):
    """One maternity record per child, with documents linked through Document."""

    employee_id = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="maternita_set")
    n_figlio = models.PositiveIntegerField(verbose_name=_("Child number"))
    nome_figlio = models.CharField(max_length=255, null=True, blank=True)
    data_comunicazione = models.DateTimeField(null=True, blank=True)
    data_prevista_parto = models.DateTimeField(null=True, blank=True)
    sedia_maternita = models.CharField(max_length=10, choices=[("SI", _("Yes")), ("NO", _("No"))], null=True, blank=True)
    sostituta = models.CharField(max_length=255, null=True, blank=True)
    id_sostituta = models.CharField(max_length=255, null=True, blank=True)
    data_nascita = models.DateTimeField(null=True, blank=True)
    data_rientro = models.DateTimeField(null=True, blank=True)
    negozio = models.CharField(max_length=255, null=True, blank=True)
    documento = models.FileField(upload_to="documents/maternita/comunicazioni/", null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["employee_id", "n_figlio"]
        constraints = [models.UniqueConstraint(fields=["employee_id", "n_figlio"], name="unique_maternity_child")]

    def __str__(self):
        return f"{self.employee_id} — {self.n_figlio}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.n_figlio:
            self.n_figlio = Maternita.objects.filter(employee_id=self.employee_id).count() + 1
        super().save(*args, **kwargs)


@receiver(m2m_changed, sender=DocumentRequest.employee_id.through)
def document_request_m2m_changed(sender, instance, action, **kwargs):
    if action == "post_add":
        document_create(instance)

    elif action == "post_remove":
        document_create(instance)


class Document(HorillaModel):
    title = models.CharField(max_length=250, blank=True, null=True)
    category = models.ForeignKey(DocumentCategory, on_delete=models.PROTECT, null=True, blank=True)
    subcategory = models.ForeignKey(DocumentSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    employee_id = models.ForeignKey(
        Employee, on_delete=models.PROTECT, verbose_name=_("Employee")
    )
    document_request_id = models.ForeignKey(
        DocumentRequest, on_delete=models.PROTECT, null=True
    )
    document = models.FileField(upload_to=document_upload_path, null=True, blank=True, verbose_name=_("Document"))
    status = models.CharField(
        choices=STATUS, max_length=10, default="requested", verbose_name=_("Status")
    )
    reject_reason = models.TextField(
        blank=True, null=True, max_length=255, verbose_name=_("Reject Reason")
    )
    issue_date = models.DateField(null=True, blank=True, verbose_name=_("Issue Date"))
    document_date = models.DateField(null=True, blank=True, verbose_name=_("Document Date"))
    start_date = models.DateField(null=True, blank=True, verbose_name=_("Start Date"))
    expiry_date = models.DateField(null=True, blank=True, verbose_name=_("Expiry Date"))
    upload_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Upload Date"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("Notes"))
    beneficiario = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Beneficiary"))
    notify_before = models.IntegerField(
        default=1, null=True, verbose_name=_("Notify Before")
    )
    is_digital_asset = models.BooleanField(
        default=False, verbose_name=_("Is Digital Asset")
    )
    maternita = models.ForeignKey("Maternita", on_delete=models.SET_NULL, null=True, blank=True, related_name="documents", verbose_name=_("Maternity"))
    objects = HorillaCompanyManager(
        related_company_field="employee_id__employee_work_info__company_id"
    )

    class Meta:
        """
        Meta class to add additional options
        """

        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def __str__(self) -> str:
        return str(self.category or self.title or f"Document {self.pk}")

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        file = self.document

        if len(self.title) < 3:
            raise ValidationError({"title": _("Title must be at least 3 characters")})

        if file and self.document_request_id:
            format = self.document_request_id.format
            max_size = self.document_request_id.max_size
            if max_size:
                if file.size > max_size * 1024 * 1024:
                    raise ValidationError(
                        {"document": _("File size exceeds the limit")}
                    )

            # Use the true final extension. A double extension such as
            # "file.pdf.html" must be rejected for a "pdf" request -- taking
            # an earlier segment (or splitext on the wrong part) would let an
            # HTML/script file through and enable stored XSS when served.
            # See GHSA-p68r-g665-5cm9.
            ext = os.path.splitext(file.name)[1].lstrip(".").lower()
            if format == "any":
                pass
            elif ext != format:
                raise ValidationError(
                    {"document": _("Please upload {} file only.").format(format)}
                )

    def save(self, *args, **kwargs):
        if not self.title and self.category:
            self.title = str(self.category)
        if self.document and not self.upload_date:
            self.upload_date = timezone.now()
        super().save(*args, **kwargs)
        if self.is_digital_asset:
            if apps.is_installed("asset"):
                from asset.models import Asset, AssetCategory

                asset_category = AssetCategory.objects.get_or_create(
                    asset_category_name="Digital Asset"
                )

                Asset.objects.create(
                    asset_name=self.title,
                    asset_purchase_date=date.today(),
                    asset_category_id=asset_category[0],
                    asset_status="Not-Available",
                    asset_purchase_cost=0,
                    expiry_date=self.expiry_date,
                    notify_before=self.notify_before,
                    asset_tracking_id=f"DIG_ID0{self.pk}",
                )

    def upload_documents_count(self):
        total_requests = Document.objects.filter(
            document_request_id=self.document_request_id
        )
        without_documents = total_requests.filter(document="").count()
        count = total_requests.count() - without_documents
        return count
