from __future__ import annotations
from typing import Literal
from django.db.models import Q
import pathlib as path 
from uuid import uuid1

# TODO Test This Function 
def genrate_image_name(instance,filename)->str:
		file_ex = path.Path(filename).suffix
		dirs = 'prodcuts/photos/'
		id = uuid1()
		product_name = instance.product.name
		return f'{dirs}{product_name}-{id}{file_ex}'


def valid_params(**kwargs)->dict:
	"""Check the Param if it doesn't ("") Or None then Return it Else Don't  """
	if kwargs:
		new = {}
		for key in kwargs:
			item = kwargs[key]
			if item is not  None and not  item == "":
				new[key] = item
		return new
	else:
		return {}



def allowed_params(allowed:tuple,**kwargs)->dict:
	"""Check the Params if they are in the allowed Tuple Remove it if doesn't Exist 
		return All allowed in Dict
		- Return Empty dict if there is no Match
		- Not Case Sensitive"""
	allowed = [ i.lower() for i in allowed ]
	if kwargs:
		new = {}
		for key in kwargs:
			if  key.lower() in allowed:
				new[key] = kwargs[key]
		return new 
	
	else:
		return {}
	

def create_lookups(key:str,dict_search:dict,connecter:Literal["OR","AND"]="AND",*args)->Q | None:
			"""Take the Value in the Dict and the Filters form args and Create Q"""
			if val:=dict_search.get(key)  :
				d = {i:val for i in args}
				q = Q(**d)
				q.connector = connecter
				return q 
			else :
				return None

