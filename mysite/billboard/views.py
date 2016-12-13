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
import calendar

# Create your views here.

def base(req):
    if(req.user.is_authenticated()):
        login_status = '1'
    else:
        login_status = '0'
    label_list = Label.objects.all()
    content_base={'label_list':label_list,'login_status':login_status,'username':req.user.username}
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
        cancer_list = []
        flag=0
        agenda = Agenda.objects.filter(user=req.user.myuser,overdue=0,checked=0)
        for i in agenda:
            if(i.activity.cancered==1):
                cancer_list.append(i.activity.title)
                flag=1
                i.checked=1
                i.overdue=1
                i.save()
        content_extend={'status':status,'flag':flag,'cancer_list':cancer_list,'newest_list':newest_list,'popular_list':popular_list}
        content_base = base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    
    def post(self,req):
        keyword = req.POST.get('keyword','')
        if(keyword!=''):
            return HttpResponseRedirect('/activitylist/?keyword=' + keyword)
        else:
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

class activitylist(TemplateView):
    template_name = "activitylist.html"
    def get(self,req):
        keyword = req.GET.get('keyword','')
        label_id =req.GET.get('label_id','')
        activity_list=[] 
        if(keyword!=''):
            activity_list=Activity.objects.filter(title__contains = keyword)
        elif(label_id!=''):
            btlalist=Bt_L_A.objects.filter(label__pk=label_id)
            for i in btlalist:
                if(i.activity not in activity_list):
                    activity_list.append(i.activity)
        else:
            activity_list=Activity.objects.all().order_by("-release")
        content_extend={'activity_list':activity_list}
        content_base = base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))

    def post(self,req):
        return HttpResponseRedirect('/login/')

class Dat(object):
    def __init__(self,useful,title,number):
        self.useful=useful
        self.title=title
        self.number=number


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
        today = datetime.date.today();
        month = req.GET.get('month','')
        year = req.GET.get('year','')
        if(month == ''):
            month = today.month
        else:
            month = int(month)
        if(year == ''):
            year = today.year
        else:
            year = int(year)
        calendar_box = calendar.monthcalendar(year,month)
        agenda = Agenda.objects.filter(user=req.user.myuser,overdue=0,activity__cancered=0)
        dat_list=[]
        days=[]
        a=0
        for i in calendar_box :
            for j in i :
                a=a+1
                if(j==0):
                    dat_list.append(Dat('data-inactive','',''))
                    days.append([])
                else:
                    that_day=datetime.date(year,month,j)
                    flag=''
                    that_day_agenda=[]
                    for r in agenda:
                        if(r.activity.pub_date==that_day):
                            flag='has a plan that day'
                            that_day_agenda.append(r)
                    dat_list.append(Dat('',flag,j))
                    days.append(that_day_agenda)
        while(a<35):
            dat_list.append(Dat('data-inactive','',''))
            days.append([])
       
        content_extend={'dat_list':dat_list,'days':days,'year':year,'month':month}
        content_base = base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    def post(self,req):
        agenda_id=req.POST.get('agenda_id','')
        edit_remark=req.POST.get('edit_remark','')
        if(agenda_id!=''):
            temp=Agenda.objects.get(pk=agenda_id)
            temp.remark=edit_remark
            temp.save()
        return HttpResponseRedirect('/myactivity/')

class postactivity(TemplateView):
    template_name = 'postactivity.html'
    def get(self,req):
        act_id = req.GET.get('activity_id','')
        if(act_id!=''):
            activity = Activity.objects.get(pk=(int(act_id)))
            stage_list = Stage.objects.filter(activity=activity).order_by("id")
            chosen_label = req.GET.get('chosen_label','')
            if(chosen_label!='' and Bt_L_A.objects.filter(discard=0,label__pk=chosen_label,activity=activity).count()==0):
                try:
                    newbtla=Bt_L_A(
                        label=Label.objects.get(pk=chosen_label),
                        activity=activity
                        )
                    newbtla.save()
                    status='btla_success'
                except:
                    status="newbtla_fail"
            else:
                status="readd_lebel"
            del_label = req.GET.get('del_label','')
            if(del_label!=''):
                del_btla=Bt_L_A.objects.get(pk=del_label)
                del_btla.discard=1
                del_btla.save()
            chosen_list = Bt_L_A.objects.filter(activity__pk=act_id,discard=0)
            content_extend = {'status':status,'chosen_list':chosen_list,'activity':activity,'activity_id':act_id,'stage_list':stage_list}
        else:
            content_extend = {'activity_id':act_id}
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
                status = 'add_act_success'
                content_extend = {'status':status,'chosen_list':[],'activity':newact,'activity_id':newact.id}
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
            chosen_list = Bt_L_A.objects.filter(activity__pk=act_id,discard=0)
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
                status='add_stage_success'
            except:
                status = 'add_stage_error'
            stage_list = Stage.objects.filter(activity=activity).order_by("id")
            content_extend = {'status':status,'chosen_list':chosen_list,'activity':activity,'activity_id':act_id,'stage_list':stage_list}
            content_base = base(req)
            content=Combine_dict(content_base,content_extend)
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))

class editactivity(TemplateView):
    template_name = 'editactivity.html'
    def get(self,req):
        del_act_id = req.GET.get('del_act_id','')
        if(del_act_id!=''):
            act=Activity.objects.get(pk=del_act_id)
            act.cancered=1
            act.save()
            return HttpResponseRedirect('/index/')

        act_id = req.GET.get('act_id','')
        if(act_id!=''):
            activity = Activity.objects.get(pk=(int(act_id)))
            stage_list = Stage.objects.filter(activity=activity).order_by("id")
            content_extend = {'status':status,'activity':activity,'act_id':act_id,'stage_list':stage}
        else:
            content_extend = {'act_id':act_id}
        content_base = base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    def post(self,req):
        if(req.POST.get('form_name','') == 'edit_act'):
            act_id = req.POST.get('edit_act_id','')
            title = req.POST.get('title','')
            introduce = req.POST.get('introduce','')
            pub_date = req.POST.get('pub_date','')
            time_start = req.POST.get('time_start','')
            time_end = req.POST.get('time_end','')
            img = req.FILES.get('img','')
         #   if(img==''):
          #      title="3333"
            act = Activity.objects.get(pk=act_id)
            act.title=title
            act.introduce=introduce
            act.pub_date=pub_date
            act.time_start=time_start
            act.time_end=time_end
            act.builder=req.user.myuser
            act.img=img
            act.save()
            stage_list = Stage.objects.filter(activity=act).order_by("id")
            content_extend = {'act_id':act_id,'stage_list':stage_list,'activity':act}
            content_base = base(req)
            content=Combine_dict(content_base,content_extend)
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))
        elif(req.POST.get('form_name','') == 'add_stage'):
            act_id = req.POST.get('act_id','')
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
                status='add_stage_success'
            except:
                status = 'add_stage_error'
            stage_list = Stage.objects.filter(activity=activity).order_by("id")
            content_extend = {'status':status,'activity':activity,'act_id':act_id,'stage_list':stage_list}
            content_base = base(req)
            content=Combine_dict(content_base,content_extend)
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))
        elif(req.POST.get('form_name','') == 'edit_stage'):
            act_id = req.POST.get('act_id','')
            stage_id = req.POST.get('edit_stage_id','')
            if(act_id == ''):
                status='no_activity'
                content_extend = {'status':status}
                content_base = base(req)
                content=Combine_dict(content_base,content_extend)
                return render_to_response(self.template_name,content,context_instance=RequestContext(req))
            activity = Activity.objects.get(pk=(int(act_id)))
            tim = req.POST.get('time','')
            brief = req.POST.get('brief','')
            subtitle = req.POST.get('subtitle','')
            stage=Stage.objects.get(pk=stage_id)
            stage.subtitle=subtitle,
            stage.brief = brief,
            stage.tim = tim,
            stage.activity = activity
            stage.save()
            stage_list = Stage.objects.filter(activity__pk=activity).order_by("id")
            content_extend = {'activity':activity,'act_id':act_id,'stage_list':stage_list}
            content_base = base(req)
            content=Combine_dict(content_base,content_extend)
            return render_to_response(self.template_name,content,context_instance=RequestContext(req))


class editactivities(TemplateView):
    template_name = 'editactivities.html'
    def get(self,req):
        activity_list=Activity.objects.filter(builder=req.user.myuser,cancered=0).order_by("-release")
        for i in activity_list:
            if(i.pub_date<datetime.date.today()):
                i.overdue=1;
                i.save()
        activity_list=Activity.objects.filter(builder=req.user.myuser,cancered=0).order_by("-release")
        content_extend = {'activity_list':activity_list}
        content_base = base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    def post(self,req):
        return HttpResponseRedirect('/index/')


class addlabel(TemplateView):
    template_name = 'addlabel.html'
    def get(self,req):
        del_id=req.GET.get('del_id','')
        if(del_id != ''):
            label=Label.objects.get(pk=del_id)
            label.delete()
        content_extend = {}
        content_base = base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    
    def post(self,req):
        name=req.POST.get('name')
        newlabel=Label(
            name=name
            )
        newlabel.save();
        content_extend = {}
        content_base = base(req)
        content=Combine_dict(content_base,content_extend)
        return render_to_response(self.template_name,content,context_instance=RequestContext(req))
    

