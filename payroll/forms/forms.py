"""
forms.py
"""

from typing import Any

from django import forms
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from base.forms import Form, ModelForm
from employee.forms import MultipleFileField
from employee.models import Employee
from payroll.context_processors import get_active_employees
from payroll.models.models import (
    Contract,
    ContractLevel,
    EncashmentGeneralSettings,
    PayrollGeneralSetting,
    ReimbursementFile,
    ReimbursementrequestComment,
)

DATE_INPUT_FORMATS = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y-%m-%d"]


class ContractForm(ModelForm):
    """
    ContactForm
    """

    verbose_name = _("Contract")
    contract_start_date = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        widget=forms.DateInput(
            format="%d/%m/%Y", attrs={"type": "text", "placeholder": "DD/MM/YYYY"}
        ),
    )
    contract_end_date = forms.DateField(
        required=False,
        input_formats=DATE_INPUT_FORMATS,
        widget=forms.DateInput(
            format="%d/%m/%Y", attrs={"type": "text", "placeholder": "DD/MM/YYYY"}
        ),
    )

    class Meta:
        """
        Meta class for additional options
        """

        fields = "__all__"
        exclude = [
            "is_active",
        ]
        model = Contract

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["employee_id"].widget.attrs.update(
            {"onchange": "contractInitial(this)"}
        )
        for field_name in ("contract_start_date", "contract_end_date"):
            self.fields[field_name].input_formats = DATE_INPUT_FORMATS
            self.fields[field_name].widget.format = "%d/%m/%Y"
            self.fields[field_name].widget.attrs.update(
                {"type": "text", "class": "oh-input w-100", "placeholder": "DD/MM/YYYY", "autocomplete": "off"}
            )
        if self.instance and self.instance.contract_start_date:
            self.initial["contract_start_date"] = self.instance.contract_start_date.strftime("%d/%m/%Y")
        if self.instance and self.instance.contract_end_date:
            self.initial["contract_end_date"] = self.instance.contract_end_date.strftime("%d/%m/%Y")
        self.fields["contract_status"].widget.attrs.update(
            {
                "class": "oh-select",
            }
        )
        if self.instance and self.instance.pk:
            dynamic_url = self.get_dynamic_hx_post_url(self.instance)
            self.fields["contract_status"].widget.attrs.update(
                {
                    "hx-target": "this",
                    "hx-post": dynamic_url,
                    "hx-swap": "beforebegin",
                }
            )
        first = PayrollGeneralSetting.objects.first()
        if first and self.instance.pk is None:
            self.initial["notice_period_in_days"] = first.notice_period
        self.fields["contract_document"].widget.attrs[
            "accept"
        ] = ".jpg, .jpeg, .png, .pdf"

    def as_p(self):
        """
        Render the form fields as HTML table rows with Bootstrap styling.
        """
        context = {"form": self}
        table_html = render_to_string("contract_form.html", context)
        return table_html

    def get_dynamic_hx_post_url(self, instance):
        """
        Render the url for contract status update through hx request
        """
        return f"/payroll/update-contract-status/{instance.pk}"


class VarzioneOrariaForm(ContractForm):
    """Contract form used to register a dated change of weekly hours."""

    verbose_name = _("Variazione Oraria")
    contratto_selezionato = forms.ModelChoiceField(
        queryset=Contract.objects.none(),
        label=_("Contratto da modificare"),
        required=True,
        empty_label=_("-- Seleziona Contratto --"),
    )

    def __init__(self, *args, contracts=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["contratto_selezionato"].queryset = (
            contracts if contracts is not None else Contract.objects.none()
        )
        self.fields["contratto_selezionato"].widget.attrs.update({"class": "oh-select"})
        self.fields["employee_id"].widget = forms.HiddenInput()
        self.fields.pop("contract_status", None)
        self.fields["attachment"] = forms.FileField(required=False, label=_("Allegato"))
        selected = self.fields.pop("contratto_selezionato")
        self.fields = {"contratto_selezionato": selected, **self.fields}

    def as_p(self):
        return render_to_string("payroll/common/variazione_oraria_contract_form.html", {"form": self})


class ContractLevelForm(ModelForm):
    """Italian contract-level history form for a single employee."""

    verbose_name = _("Livello")
    data_decorrenza = forms.DateField(
        input_formats=DATE_INPUT_FORMATS,
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={"type": "text", "placeholder": "DD/MM/YYYY", "autocomplete": "off"},
        ),
    )

    class Meta:
        model = ContractLevel
        fields = ["employee_id", "lvl", "data_decorrenza", "note"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["employee_id"].widget = forms.HiddenInput()
        self.fields["lvl"].widget.attrs.update(
            {"class": "oh-input w-100", "min": 0, "step": 1}
        )
        self.fields["note"].required = False
        self.fields["note"].widget.attrs.update({"class": "oh-input w-100", "rows": 3})
        if self.instance and self.instance.data_decorrenza:
            self.initial["data_decorrenza"] = self.instance.data_decorrenza.strftime(
                "%d/%m/%Y"
            )


class ReimbursementRequestCommentForm(ModelForm):
    """
    ReimbursementRequestCommentForm form
    """

    class Meta:
        """
        Meta class for additional options
        """

        model = ReimbursementrequestComment
        fields = ("comment",)


class reimbursementCommentForm(ModelForm):
    """
    Reimbursement request comment model form
    """

    verbose_name = "Add Comment"

    class Meta:
        """
        Meta class for additional options
        """

        model = ReimbursementrequestComment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["files"] = MultipleFileField(label="files")
        self.fields["files"].required = False
        self.fields["files"].widget.attrs["accept"] = ".jpg, .jpeg, .png, .pdf"

    def as_p(self):
        """
        Render the form fields as HTML table rows with Bootstrap styling.
        """
        context = {"form": self}
        table_html = render_to_string("common_form.html", context)
        return table_html

    def save(self, commit: bool = ...) -> Any:
        multiple_files_ids = []
        files = None
        if self.files.getlist("files"):
            files = self.files.getlist("files")
            self.instance.attachemnt = files[0]
            multiple_files_ids = []
            for attachemnt in files:
                file_instance = ReimbursementFile()
                file_instance.file = attachemnt
                file_instance.save()
                multiple_files_ids.append(file_instance.pk)
        instance = super().save(commit)
        if commit:
            instance.files.add(*multiple_files_ids)
        return instance, files


class EncashmentGeneralSettingsForm(ModelForm):
    class Meta:
        model = EncashmentGeneralSettings
        fields = "__all__"


class DashboardExport(Form):
    status_choices = [
        ("", ""),
        ("draft", "Draft"),
        ("review_ongoing", "Review Ongoing"),
        ("confirmed", "Confirmed"),
        ("paid", "Paid"),
    ]
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "oh-input w-100"}),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "oh-input w-100"}),
    )
    employees = forms.ChoiceField(
        required=False,
        choices=[(emp.id, emp.get_full_name()) for emp in Employee.objects.all()],
        widget=forms.SelectMultiple,
    )
    status = forms.ChoiceField(required=False, choices=status_choices)
    contributions = forms.ChoiceField(
        required=False,
        choices=[
            (emp.id, emp.get_full_name())
            for emp in get_active_employees(None)["get_active_employees"]
        ],
        widget=forms.SelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["employees"].widget.attrs.update({"class": "oh-select oh-select-2"})
        self.fields["status"].widget.attrs.update({"class": "oh-select oh-select-2"})
        self.fields["contributions"].widget.attrs.update(
            {"class": "oh-select oh-select-2"}
        )
