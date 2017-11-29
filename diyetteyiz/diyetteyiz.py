# -*- coding:utf-8 -*-
# Diyetteyiz app
from openerp import models, fields , api

#Extend product.template model with calories
class diyetteyiz_product_template(models.Model):
    _name = 'product.template'
    _inherit='product.template'
    
    #burada modeli inherit edip genişlettik 

    calories = fields.Integer("Calories")
    servingsize = fields.Float('Serving Size')
    lastupdated = fields.Date('Last Updated')
    nutrient_ids = fields.One2many('product.template.nutrient','product_id','Nutrients') ## bir üründe birden fazla besin olabilir
    
    ## yiyecekteki toplam besin değerini hesaplayan metod
    @api.one
    @api.depends('nutrient_ids','nutrient_ids.value') # değiştiğinde tetiklenecek değerler
    def _calcscore(self):
        currentscore = 0
        for nutrient in self.nutrient_ids:
            if nutrient.nutrient_id.name == 'Protein':
                currentscore= currentscore+(nutrient.value * 5)
            else:
                currentscore+=nutrient.value     
        self.nutrition_score = currentscore
    
    nutrition_score = fields.Float(string="Nutrition Score",store=True, compute="_calcscore") ## yeni bir field _calcscore fonksiyonunda heasplanacak
    

class diyetteyiz_res_users_meal(models.Model):    
    # burada ise aşağıdaki isimle yeni model oluşturduk   
    _name="res.users.meal"
    name = fields.Char("Meal Name")
    meal_date = fields.Datetime("Meal Date")
    item_ids=fields.One2many('res.users.mealitem','meal_id') #( obje adı - ilişkili id - field name ) ## bir yemekte birden fazla item olabilir
    user_id=fields.Many2one('res.users',"Meal User")
    
    largemeal= fields.Boolean("Large Meal")   
    ## total calories alanı değiştiğinde daha veritabanına gitmeden, 
    ## gerçekleşecek olan değişiklik kullanıcı arayüzünde görünecek
    @api.onchange('totalcalories')
    def check_totalcalories(self):
        if self.totalcalories > 500:
            self.largemeal=True
        else:
            self.largemeal=False
    
    
    totalcalories=fields.Integer(string="Total Calories",store=True,compute="_calccalories")   
    # toplam yiyecek kalorisini hesaplayan metod 
    @api.one
    @api.depends('item_ids','item_ids.servings') # değiştiğinde tetiklenecek değerler
    def _calccalories(self):
        currentCalories = 0
        for mealitem in self.item_ids:
            currentCalories+= (mealitem.calories * mealitem.servings)        
        self.totalcalories = currentCalories
    
    notes = fields.Text('Meal Notes')  
   
# yemek öğelerini tutacak model
class diyetteyiz_res_users_mealitems(models.Model):
    _name = 'res.users.mealitem'
    meal_id = fields.Many2one('res.users.meal')
    item_id = fields.Many2one('product.template','Meal Item')
    servings=fields.Float('Servings')
    calories = fields.Integer(related="item_id.calories",string="Calories Per Serving",store=True,readonly=True)
    notes = fields.Text("Meal Item Notes")
    

class diyetteyiz_product_nutrient(models.Model):
    _name='product.nutrient' # oluşturduğumuz yeni modelin adı
    name=fields.Char("Nutrient Name")
    uom_id=fields.Many2one('product.uom','Unit of Measure') # ölçü birimleriyle ilişkilendiriyoruz
    description = fields.Text("Description")
    

class diyetteyiz_product_template_nutrient(models.Model):
    _name="product.template.nutrient"
    nutrient_id =  fields.Many2one('product.nutrient',string="Product Nutrient")
    product_id = fields.Many2one('product.template')
    uom = fields.Char(related='nutrient_id.uom_id.name',string="Birimi",readonly=True) ## besinin ölçü birimini göstermek için
    value = fields.Float('Nutrient Value')
    dailypercent = fields.Float('Daily Recommended Value')
    
    
    
    
    
    