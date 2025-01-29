from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import requests
from django.contrib.auth import login, authenticate,logout
from django.views.generic import View
from django.core.paginator import Paginator


# --------------------------------------------- global --------------------------------------------------------------------
url = "http://10.20.50.117:8080/graphql/"




def request_from_end_point(request,payload):
    token = request.session.get('token')
    # print("\n At top--- ",token)
    token_1 = f'Bearer {token}'
    headers = {
                    'Authorization': token_1,
                    'Content-Type': 'application/json'
                }
    response = requests.request("POST", url, headers= headers, data=payload)
    
    # print("\npaload*********  ",payload)
    # print("\nheaders********  ",response.headers)
    
    json_data = response.json()
    # print("\nrequest_from_end_point (json_data**********   ",  json_data)
    
    key = 'Token-Expired'
  
    if key in response.headers:
        refreshToken(request,payload)
        
    # if token == key:
    #     print("******************")
    #     return logout_request(request)

    # print('final step')
    return json_data

#---------------------------------------------------- Refresh Token ---------------------------------------------------------------
def refreshToken(request,payload):
  
    token = request.session.get('token')
    
    token_1 = f'Bearer {token}'
    refreshtoken = request.session.get('refresh_token')
    
    payload_ ="{\"query\":\"{\\r\\n  refreshToken(token: \\\""+str(token)+"\\\" ,refreshtoken: \\\""+str(refreshtoken)+"\\\"){\\r\\n    tokenStr\\r\\n  refreshToken\\r\\n   }\\r\\n}\",\"variables\":{}}"
    
    headers = {
                    'Authorization': token_1,
                    'Content-Type': 'application/json'
                }
    
    response_1 = requests.request("POST", url, headers= headers, data=payload_).json()
    # response_1 = request_from_end_point(request,payload_)
    
    # print("refreshtoken response--- ", response_1)
            
    request.session['token'] = response_1['data']['refreshToken']['tokenStr']
    request.session['refresh_token'] = response_1['data']['refreshToken']['refreshToken'] 
    
    return request_from_end_point(request,payload)

#----------------------------------------------------- show data for ajax --------------------------------------------------------
def ajax_show_data(request):
    userId = request.session.get('user_id')
    print("user_id= ",userId)
    payload="{\"query\":\"{\\r\\n  riskProfileMasters (entryBy:"+str(userId)+"){\\r\\n    riskId\\r\\n    riskProfile\\r\\n  isActive\\r\\n  entryBy\\r\\n   doe\\r\\n  modifiedBy\\r\\n  dateModified\\r\\n}\\r\\n}\",\"variables\":{}}"
 
    json_data = request_from_end_point(request,payload)
    
    return json_data

#--------------------------------------------------- Display ------------------------------------------------------------------------
def display_mutation(request):
    json_data = ajax_show_data(request)
    return render(request,'risk_profile_app/add_mutation.html',{'json_data':json_data})

# ------------------------------------------------ pagination ------------------------------------------------------------
    # paginator = Paginator(json_data['data']['riskProfileMasters'],10)              #limit to data
    # page_number = request.GET.get('page')      #get page number
    # page_obj = paginator.get_page(page_number)
    # last_page = page_obj.paginator.num_pages
    # total_page_list = [n+1 for n in range(last_page)]

    #'page_obj':page_obj,'last_page':last_page,'total_page_list':total_page_list})
    
#------------------------------------------------ Add --------------------------------------------------------------------------
def add_mutation(request):
        
        userId = str(request.session.get('user_id'))
    
        if request.method == "POST":
            nm = request.POST.get('name')
            
            payload="{\"query\":\"mutation{\\r\\n  createRiskProfileMaster(entryBy:"+str(userId)+", riskProfile:\\\""+nm+"\\\"){\\r\\n    riskProfile\\r\\n    riskId\\r\\n  }\\r\\n}\",\"variables\":{}}"
            
            json_Add_data = request_from_end_point(request,payload)
            
            # return redirect("/display_mutation")
        # return render(request,'add_mutation.html')
        response_1 = ajax_show_data(request)
        
        return JsonResponse({'status':'save','response_1':response_1})
  
#-------------------------------------------------- delete --------------------------------------------------------------------------
def delete_mutation(request,id):
    
    str_id = str(id)
    userId = str(request.session.get('user_id'))
   
    payload="{\"query\":\"mutation{\\r\\n  deleteRiskProfileMaster(riskId:"+str_id+", modifiedBy: "+str(userId)+")\\r\\n}\",\"variables\":{}}"
    
    json_delete_data = request_from_end_point(request,payload)
    
    return redirect("/display_mutation")

# ------------------------------------------- Delete using ajax -------------------------------------------------------------------------
def delete_ajax(request):
    if request.method == "POST":
        id = request.POST.get('id')
        delete_mutation(request,id)
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

# #----------------------------------------------- go_update----------------------------------------------------------------------
# def go_update(request,id,name_1):
#     return render(request,'update_mutation.html',{'id':id,'name_1':name_1})

#----------------------------------------------------- update mutation --------------------------------------------------------
def update_mutation(request,id):
        
    userId = str(request.session.get('user_id'))
    
    if request.method == "POST":
        nm = request.POST.get('name')
        risk_id = str(id)

        payload="{\"query\":\"mutation{\\r\\n  updateRiskProfileMaster(riskId: "+ risk_id +", riskProfile:\\\""+nm+"\\\",modifiedBy: "+str(userId)+"){\\r\\n    riskProfile\\r\\n    riskId\\r\\n  entryBy\\r\\n  modifiedBy\\r\\n}\\r\\n}\",\"variables\":{}}"
       
        json_update_data =  request_from_end_point(request,payload)
       
        # return redirect("/display_mutation")
    # return render(request,'update_mutation.html')
    
    return JsonResponse({'status':1,'json_update_data':json_update_data})  
    
# -------------------------------------------- update data for ajax ---------------------------------------------------------
def edit_ajax(request):
        
    userId = request.session.get('user_id')
    
    if request.method == "POST":
        nm = request.POST.get('name')
        print("=======",nm)
        risk_id = str(request.POST.get('id'))
        
        payload="{\"query\":\"mutation{\\r\\n  updateRiskProfileMaster(riskId: "+ risk_id +" riskProfile:\\\""+nm+"\\\" modifiedBy: "+str(userId)+"){\\r\\n    riskProfile\\r\\n    riskId\\r\\n  entryBy\\r\\n  modifiedBy\\r\\n}\\r\\n}\",\"variables\":{}}"
        
        json_update_data = request_from_end_point(request,payload)
          
        # return redirect("/display_mutation")
    response_1 = ajax_show_data(request)
    
    return JsonResponse({'status':1,'json_update_data':json_update_data,'response_1':response_1})  

#----------------------------------------------------- pdf ----------------------------------------------------------------------
class GeneratePdf(View):
    pass
    # def get(self, request, *args, **kwargs):
        
   
    #     data = {
    #          'employee':
    #     }
        
    #     # pdf = render_to_pdf('show.html', data)
        
    #     template = get_template('add_mutation.html')
    #     html  = template.render(data)
        
    #     result = BytesIO()
        
    #     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        
    #     if not pdf.err:
    #         response =  HttpResponse(result.getvalue(), content_type='application/pdf')
    #         response['Content-Disposition']='attachment;filename = "mutationfile.pdf"'
    #         return response
    #     return None
    
#----------------------------------------- delete selected checkbox ---------------------------------------------------------
def delete_selected(request,*args,**kwargs):
    if request.method == "POST":
        client_ids = request.POST.getlist('id[]')
        print(client_ids)
        for i in client_ids:
            print(i)
            client = delete_mutation(request,i)

    return JsonResponse({'status':1})




