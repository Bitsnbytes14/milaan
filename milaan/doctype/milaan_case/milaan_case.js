frappe.ui.form.on("Milaan Case", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button("Assign to me", () => {
				frappe.call({ method: "milaan.api.assign_case", args: { case_name: frm.doc.name, user: frappe.session.user }, callback: () => frm.reload_doc() });
			});
			frm.add_custom_button("Assign", () => frm.trigger("assign_case"));
			if (frm.doc.status !== "Resolved") {
				frm.add_custom_button("Resolve", () => frm.trigger("resolve_case"));
			} else {
				frm.add_custom_button("Reopen", () => frappe.call({ method: "milaan.api.reopen_case", args: { case_name: frm.doc.name }, callback: () => frm.reload_doc() }));
			}
		}
	},
	assign_case(frm) {
		frappe.prompt({ fieldtype: "Link", fieldname: "user", label: "Assign to", options: "User", reqd: 1 }, values => {
			frappe.call({ method: "milaan.api.assign_case", args: { case_name: frm.doc.name, user: values.user }, callback: () => frm.reload_doc() });
		}, "Assign case");
	},
	resolve_case(frm) {
		frappe.prompt({ fieldtype: "Small Text", fieldname: "notes", label: "Resolution notes", reqd: 1 }, values => {
			frappe.call({ method: "milaan.api.resolve_case", args: { case_name: frm.doc.name, resolution_notes: values.notes }, callback: () => frm.reload_doc() });
		}, "Resolve case");
	},
});
