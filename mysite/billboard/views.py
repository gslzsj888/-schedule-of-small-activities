from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator

# Create your views here.

def POST_base(req):
    if(req.user.is_authenticated()):
        login_status = '1'
    else:
        login_status = '0'
    content_base={'login_status':login_status}
    return content_base

def GET_base(req):
    if(req.user.is_authenticated()):
        login_status = '1'
    else:
        login_status = '0'
    content_base={'login_status':login_status}
    return content_base

class login(TemplateView):
	template_name = "login.html"
	def get(self,req):
        if(req.user.is_authenticated() == 1):
            return HttpResponseRedirect('/index/')
        state = ''
        content_extend={'status':state}
        content_base = GET_base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    def post(self,req):
    	if(req.POST.get('form_name','') == 'login'):
    		username = req.POST.get('username','')
        	password = req.POST.get('passwd','')
       	 	user = auth.authenticate(username = username,password = password)
        	if(user is None):
            	status = 'login_error'
            	content_extend={'status':status}
            	content_base = POST_base(req)
            	content=Combine_dict(content_base,content_extend)
            	return render_to_response(self.template_name,content,context_instance=RequestContext(req))
        	else:
            	auth.login(req,user)
            	return HttpResponseRedirect('/index/')
     	elif(req.POST.get('form_name','') == 'signup'):
     		username = req.POST.get('username','')
        	password = req.POST.get('passwd','')
        	repassword = req.POST.get('repasswd','')
        	email = req.POST.get('email','')
        	if((username == '') or (password == '') or (repassword == '') or (email == '')):
            	status = 'error'
        	elif(password!=repassword):
            	status = 're_error'
        	elif(User.objects.filter(username = username).count()!=0):
            	status = 'user_exist'
        	else:
            	newuser=User.objects.create_user(
                	username = username,
                	password = password
                	)
            	newuser.save()
            	newMyuser=Myuser(
                	user = newuser,
                	email = email
                	)
            	newMyuser.save()
            	status = 'success'
        	content_extend = {'status':status}
        	content_base = POST_base(req)
        	content=Combine_dict(content_base,content_extend)
        	return render_to_response(self.template_name,content,context_instance=RequestContext(req))

class logout(TemplateView):
    def get(self,req):
        auth.logout(req)
        return HttpResponseRedirect('/index/')

class index(TempleteView):
	template_name = "index.html"
    def get(self,req):
    	newest_list = Activity.objects.order_by("－release")[0:4]
    	popular_list = Activity.objects.order_by("-popular")[0:4]
        content_extend = {'newest_list':newest_list, 'popular_list':popular_list}
        content_base = GET_base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
	def post(self,req):
		if(req.POST.get('form_name','') == 'add_agenda'):
			select_act = req.POST.get('select_id','')
			try:
				if(Agenda.objects.filter(activity__pk=select_act,user=req.user.myuser).Count()==0):
					newagenda=Agenda(
                		user = req.user.myuser,
                		activity = Activity.object.get(pk=select_act)
                		)
            		newagenda.save()
            		activity=Activity.object.get(pk=select_act);
            		activity.popular =activity.popular+1;
            		activity.save();
            		status = 'success'
				else:
					status = 're_add'
			except:
                status = 'error'
            content_extend = {'status':status}
        	content_base = POST_base(req)
            content=Combine_dict(content_base,content_extend)
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))
        	
class activity(TempleteView):
	template_name = "activity.html"
    def get(self,req):
        view_act = req.GET.get('view_id','')
        if(view_act == ''):
            return HttpResponseRedirect('/index/')
        try:
            activity = Activity.objects.get(pk=view_act)
			stage = activity.stage.all()
			stage.sort(key=lambda x:x.id)  
        except:
            return HttpResponseRedirect('/index/')
        content_extend={'activity' : activity,'stage':stage}
        content_base = GET_base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
	def post(self,req):
		if(req.POST.get('form_name','') == 'add_agenda'):
			select_act = req.POST.get('select_act','')
			try:
				if(Agenda.objects.filter(activity__pk=select_act,user=req.user.myuser).count()==0):
					newagenda=Agenda(
                		user = req.user.myuser,
                		activity = Activity.object.get(pk=select_act)
                		)
            		newagenda.save()
            		status = 'success'
				else:
					status = 're_add'
			except:
                status = 'error'
            content_extend = {'status':status}
        	content_base = POST_base(req)
            content=Combine_dict(content_base,content_extend)
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))

class myactivity(TempleteView):
	template_name = 'myactivity.html'
	def get(self,req):
		Agenda = Agenda.objects.filter(user=req.user.myuser,overdue=0,checked=0)
		change_list = []
		today_agenda = []
		all_agenda = []
		for i in Agenda:
			if(i.pub_date<datetime.now.today()):
				i.overdue=1
				i.save()
			elif(i.activity.cancered==1):
				change_list.append(i)
			else:
				all_agenda.append(i)
				if(i.pub_date = datetime.now.today()):
					stage = i.activity.stage.all()
					stage.sort(key=lambda x:x.id)  
					today_agenda.append((i,stage))
        content_extend={'change_list':change_list,'today_agenda':today_agenda,'all_agenda':all_agenda}
        content_base = GET_base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
     def post(self,req):
     	if(req.POST.get('form_name','') == 'delete'):
       		del_agenda = req.POST.get('del_agenda','')
       		agenda = Agenda.objects.get(pk=del_agenda)
       		agenda.overdue=1;
       		agenda.save();
	
class postactivity(TempleteView):
	template_name = 'postactivity.html'
	def get(self,req):
        act_id = req.POST.get('activity_id','')
       	activity = Activity.objects.get(pk=act_id)
		stage = activity.stage.all()
		stage.sort(key=lambda x:x.id)  
        content_extend = {'activity':activity,'stage':stage}
        content_base = GET_base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    def post(self,req):
    	if(req.POST.get('form_name','') == 'add_act'):
       	 	title = req.POST.get('title','')
        	introduce = req.POST.get('introduce','')
        	pub_date = req.POST.get('pub_date','')
        	time_start = req.POST.get('time_start','')
        	time_end = req.POST.get('time_end','')
       	 	img = req.FILES.get('img','')
       		try:
        		newact=Activity(
        			title=title,
        			introduce=introduce,
        			pub_date=pub_date,
        			time_start=time_start,
        			time_end=time_end,
        			builder=req.user.myuser,
        			img=img
        			)
            	newact.save()
            	status = 'success'
            except :
                status = 'error'
        	content_extend = {'status':status,'activity':newact}
        	content_base = POST_base(req)
        	content=Combine_dict(content_base,content_extend)
        	return render_to_response(self.template_name,content,context_instance=RequestContext(req))
        elif(req.POST.get('form_name','') == 'add_stage'):
        	act_id = req.POST.get('activity_id','')
        	tim = req.POST.get('time','')
        	brief = req.POST.get('brief','')
        	subtitle = req.POST.get('subtitle','')
        	activity = Activity.objects.get(pk=act_id)
        	try:
        		newstage=Stage(
        			subtitle=subtitle,
        			brief = brief,
					tim = tim,
					activity = activity
        			)
        		newstage.save()
        		status='success'
			except :
                status = 'error'
        	content_extend = {'status':status,'activity':newact}
        	content_base = POST_base(req)
        	content=Combine_dict(content_base,content_extend)
        	return render_to_response(self.template_name,content,context_instance=RequestContext(req))
       
