#Human Resources App

from openerp import models,fields,api


GENDER = [
          ('male','Male'),
          ('female','Female')
         ]
TYPE = [('trainee','Trainee'),
        ('probation','Probation'),
        ('employee','Employee')
        ]
class employee_employee(models.Model):
    _name="mechsoft.employee"
    _description = "Employeee Details"
    
    name = fields.Char(string="Name", required=True)
    emp_id = fields.Char("Employee ID")
    image = fields.Binary("Image")
    age=fields.Integer(string="Age")
    active = fields.Boolean(string="Active",default=1)
    basic = fields.Float(string="Basic")
    bdate = fields.Datetime(string="Birth Date")
    jdate = fields.Datetime(string="Join Date")
    notes = fields.Text(string="Notes")
    template = fields.Html(string="Template")
    gender = fields.Selection(GENDER,"Gender",default='male')
    
    department_id = fields.Many2one("mechsoft.department","Department")
    ref_ids=fields.One2many("reference_detail","employee_id","References")
    hobbies_ids = fields.Many2many("hobbies.detail",
                                   "employee_hobbies_rel",
                                   "emp_id",
                                   "hobbie_id",
                                   string="Hobbies Info")
    
    responsible_id=fields.Many2one("res.partner","Responsible Person")
    email = fields.Char(related="responsible_id.email",string="Resp Email",)
    phone = fields.Char(related="responsible_id.phone",string="Resp Contact",)
    ref = fields.Reference(selection=[('res.partner','Partner'),
                                      ('res.users','User'),
                                      ('mechsoft.employee','Employee'),])
    
    type_emp=fields.Selection(TYPE,'Employee Type',default="probation")
    ref_link = fields.Char("External Link")
    
    
class my_department(models.Model):
    _name = "mechsoft.department"
    _description="Departments"
    
    code = fields.Char("Code")
    name = fields.Char("Name")
    
class reference_detail(models.Model):
    
    _name="reference_detail"
    
    employee_id = fields.Many2one("mechsoft.employee","Employee",ondelete="cascade")
    name=fields.Char("Name")
    contact = fields.Char("Contact Number")
    email = fields.Char("Email")
    
class hobbies_detail(models.Model):
    _name="hobbies.detail"
    
    hobbie_id=fields.Char("Hobbie ID")
    name=fields.Char("Name")
    
    
    
    
