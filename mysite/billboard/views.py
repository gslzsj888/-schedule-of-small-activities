from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
import datetime

# Create your views here.

def base(req):
    if(req.user.is_authenticated()):
        login_status = '1'
    else:
        login_status = '0'
    content_base={'login_status':login_status,'username':req.user.username}
    return content_base


def Combine_dict(dict1,dict2):
    dict3 ={}
    for i in dict1.keys():
        dict3[i] = dict1[i]
    for i in dict2.keys():
        dict3[i] = dict2[i]
    return dict3

class login(TemplateView):
    template_name = "login.html"
    def get(self,req):
        if(req.user.is_authenticated()):
            return HttpResponseRedirect('/index/')
        status = ''
        content_extend={'status':status}
        content_base = base(req)
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
            	content_base = base(req)
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
            	newmyuser=MyUser(
                	user = newuser,
                	email = email
                	)
            	newmyuser.save()
            	status = 'success'
            content_extend = {'status':status}
            content_base = base(req)
            content=Combine_dict(content_base,content_extend)
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))

class logout(TemplateView):
    def get(self,req):
        auth.logout(req)
        return HttpResponseRedirect('/login/')

class index(TemplateView):
    template_name = "iindex.html"
    def get(self,req):
        view_act = req.GET.get('view_id','')
        if(view_act!=''):
            return HttpResponseRedirect('/activity/?view_id='+view_act)
        newest_list = Activity.objects.order_by("-release")[0:4]
        popular_list = Activity.objects.order_by("-popular")[0:4]
        status=''
        select_act=req.GET.get('select_id','')
        if(select_act!=''):
            try:
                if(Agenda.objects.filter(activity__pk=select_act,overdue=0,user=req.user.myuser).count()==0):
                    newagenda=Agenda(
                        user = req.user.myuser,
                        activity = Activity.objects.get(pk=select_act)
                        )
                    newagenda.save()
                    activity=Activity.objects.get(pk=select_act)
                    activity.popular =activity.popular+1
                    activity.save()
                    status = 'success'
                else:
                    status = 're_add'
            except:
                status = 'error'
        content_extend={'status':status,'newest_list':newest_list,'popular_list':popular_list}
        content_base = base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    
    def post(self,req):
        return HttpResponseRedirect('/index/')

class activity(TemplateView):
    template_name = "activity.html"
    def get(self,req):
        select_act=req.GET.get('select_id','')
        if(select_act!=''):
            try:
                if(Agenda.objects.filter(activity__pk=select_act,overdue=0,user=req.user.myuser).count()==0):
                    newagenda=Agenda(
                        user = req.user.myuser,
                        activity = Activity.objects.get(pk=select_act)
                        )
                    newagenda.save()
                    activity=Activity.objects.get(pk=select_act)
                    activity.popular =activity.popular+1
                    activity.save()
                    status = 'success'
                else:
                    status = 're_add'
            except:
                status = 'error'
            return HttpResponseRedirect('/activity/?view_id='+select_act)
        view_act = req.GET.get('view_id','')
        try:
            activity = Activity.objects.get(pk=view_act)
            stage_list = Stage.objects.filter(activity=activity).order_by("id")
        except:
            return HttpResponseRedirect('/index/')
        content_extend={'activity':activity,'stage_list':stage_list}
        content_base = base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    def post(self,req):
        return HttpResponseRedirect('/login/')


class myactivity(TemplateView):
    template_name = 'myactivity.html'
    def get(self,req):
        del_agenda=req.GET.get('del_id','')
        if(del_agenda!=''):
            agenda = Agenda.objects.get(pk=del_agenda)
            agenda.overdue=1
            agenda.save()
            agenda.activity.popular=agenda.activity.popular-1
            return HttpResponseRedirect('/myactivity/')
        agenda = Agenda.objects.filter(user=req.user.myuser,overdue=0,checked=0)
        change_list = []
        today_agenda = []
        all_agenda = []
        for i in agenda:
            if(i.activity.pub_date<datetime.date.today()):
                i.overdue=1
                i.save()
            elif(i.activity.cancered==1):
                change_list.append(i)
            else:
                all_agenda.append(i)
                if(i.activity.pub_date == datetime.date.today()):
                    stage_list = Stage.objects.filter(activity=i.activity).order_by("id")
                    for j in stage_list:
                        today_agenda.append(j)
        content_extend={'change_list':change_list,'today_agenda':today_agenda,'all_agenda':all_agenda}
        content_base = base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    def post(self,req):
        return HttpResponseRedirect('/myactivity/')

class postactivity(TemplateView):
    template_name = 'spostactivity.html'
    def get(self,req):
        act_id = req.POST.get('activity_id','')
        if(act_id!=''):
            activity = Activity.objects.get(pk=(int(act_id)))
            stage_list = Stage.objects.filter(activity=activity).order_by("id")
            content_extend = {'activity':activity,'activit_id':act_id,'stage_list':stage}
        else:
            content_extend = {'activit_id':act_id}
        content_base = base(req)
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
         #   if(img==''):
          #      title="3333"
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
                content_extend = {'status':status,'activity':newact,'activity_id':newact.id,'user':req.user.username}
            except:
                status = 'add_act_error'
                content_extend = {'status':status}
            content_base = base(req)
            content=Combine_dict(content_base,content_extend)
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))
        elif(req.POST.get('form_name','') == 'add_stage'):
            act_id = req.POST.get('activity_id','')
            if(act_id == ''):
                status='no_activity'
                content_extend = {'status':status}
                content_base = base(req)
                content=Combine_dict(content_base,content_extend)
                return render_to_response(self.template_name,content,context_instance=RequestContext(req))
            tim = req.POST.get('time','')
            brief = req.POST.get('brief','')
            subtitle = req.POST.get('subtitle','')
            activity = Activity.objects.get(pk=(int(act_id)))
            try:
                newstage=Stage(
                    subtitle=subtitle,
                    brief = brief,
                    tim = tim,
                    activity = activity
                    )
                newstage.save()
                status='success'
            except:
                status = 'add_stage_error'
            stage_list = Stage.objects.filter(activity=activity).order_by("id")
            content_extend = {'status':status,'activity':activity,'activity_id':act_id,'stage_list':stage_list}
            content_base = base(req)
            content=Combine_dict(content_base,content_extend)
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))