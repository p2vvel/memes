from datetime import datetime, timedelta
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from .forms import MemeForm
from .models import Category, Meme, MemeKarma
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from comments.forms import MemeCommentForm
from django.db.models import Q


# main site with accepted memes
class MainMemeView(ListView):
    model = Meme
    paginate_by = 8
    template_name = "memes/main_view.html"
    context_object_name = "memes"
    ordering = ["-date_accepted"]

    def get_queryset(self):
        user = get_user(self.request)
        data = super().get_queryset()
        data = data.filter(accepted=True, hidden=False)
        if self.request.user.is_authenticated:
            for k in data:
                k.karma_given = k.is_karma_given(user)
        else:
            for k in data:
                k.karma_given = False

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MemeForm()
        return context


class NewMainMemeView(ListView):
    model = Meme
    paginate_by = 8
    template_name = "memes/category_view.html"
    context_object_name = "memes"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewMainMemeView, self).get_context_data()
        context["sort_methods"] = [("new", "New"), ("best", "Best"), ("best12", "Best 12h"), ("best72", "Best 72h")]
        return context

    def get_queryset(self):
        """Get memes without category"""
        data = self.model.objects.filter(accepted=True, hidden=False, category=None)    #getting base memes list

        sort_method = self.request.GET.get("sort", "new")
        if sort_method == "best":
            data = data.order_by("-karma")
        elif sort_method == "best12":
            time_delta = timezone.now() - timedelta(hours=12)
            data = data.order_by("-karma").filter(date_accepted__gte=time_delta)
        elif sort_method == "best72":
            time_delta = timezone.now() - timedelta(days=3)
            data = data.order_by("-karma").filter(date_accepted__gte=time_delta)
        else:   # sort_method == "new":
            data = data.order_by("-date_accepted")

        # adding information to indicate if user has given a karma point to the meme
        user = get_user(self.request)
        if self.request.user.is_authenticated:
            for k in data:
                k.karma_given = k.is_karma_given(user)
        else:
            for k in data:
                k.karma_given = False
        return data



@method_decorator(csrf_exempt, name='dispatch')
class FreshMemeView(ListView):
    model = Meme
    paginate_by = 8
    template_name = "memes/fresh_view.html"
    context_object_name = "memes"

    def get_queryset(self):
        """Sorting and filtering memes by category"""
        data = self.model.objects.filter(accepted=False, hidden=False)    #getting base data

        if not self.request.user.is_authenticated:
            condition = Q(category__isnull=True) | Q(category__public=True)
            data = data.filter(condition)

        chosen_categories = self.request.GET.getlist("category")    # getting categories
        try:
            chosen_categories[chosen_categories.index("none")] = None   # replace "none" string with real none value
        except ValueError:
            pass    # nothing to do if user doesn't want to see main memes (those without assigned category),
                    # error raised if "none" not in chosen categories

        if chosen_categories != []:
            categories_filter = Q()
            for k in chosen_categories:
                categories_filter |= Q(category__slug__iexact=k)
            data = data.filter(accepted=False).filter(categories_filter)

        sort_method = self.request.GET.get("sort", "new")
        if sort_method == "best":
            data = data.order_by("-karma")
        elif sort_method == "best12":
            time_delta = timezone.now() - timedelta(hours=12)
            data = data.order_by("-karma").filter(date_created__gte=time_delta)
        elif sort_method == "best72":
            time_delta = timezone.now() - timedelta(days=3)
            data = data.order_by("-karma").filter(date_created__gte=time_delta)
        else:   # sort_method == "new":
            data = data.order_by("-date_created")

        # adding information to indicate if user has given a karma point to the meme
        user = get_user(self.request)
        if self.request.user.is_authenticated:
            for k in data:
                k.karma_given = k.is_karma_given(user)
        else:
            for k in data:
                k.karma_given = False
        return data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FreshMemeView, self).get_context_data()
        if self.request.user.is_authenticated:
            categories = Category.objects.all()
        else:
            categories = Category.objects.filter(public=True)
        context["categories"] = categories
        context["sort_methods"] = [("new", "New"), ("best", "Best"), ("best12", "Best 12h"), ("best72", "Best 72h")]
        return context


class CategoryView(ListView):
    model = Meme
    paginate_by = 8
    template_name = "memes/category_view.html"
    context_object_name = "memes"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryView, self).get_context_data()
        context["sort_methods"] = [("new", "New"), ("best", "Best"), ("best12", "Best 12h"), ("best72", "Best 72h")]
        return context

    def get_queryset(self):
        """Get memes from chosen category"""
        category = get_object_or_404(Category, slug__iexact=self.kwargs["category"])    #getting category
        if not self.request.user.is_authenticated and not category.public:
            raise Http404()     #raise 404 if category shouldnt be visible for anonumous users

        data = self.model.objects.filter(accepted=True, hidden=False, category=category)    #getting base memes list

        sort_method = self.request.GET.get("sort", "new")
        if sort_method == "best":
            data = data.order_by("-karma")
        elif sort_method == "best12":
            time_delta = timezone.now() - timedelta(hours=12)
            data = data.order_by("-karma").filter(date_accepted__gte=time_delta)
        elif sort_method == "best72":
            time_delta = timezone.now() - timedelta(days=3)
            data = data.order_by("-karma").filter(date_accepted__gte=time_delta)
        else:   # sort_method == "new":
            data = data.order_by("-date_accepted")

        # adding information to indicate if user has given a karma point to the meme
        user = get_user(self.request)
        if self.request.user.is_authenticated:
            for k in data:
                k.karma_given = k.is_karma_given(user)
        else:
            for k in data:
                k.karma_given = False
        return data


class MemeView(DetailView):
    model = Meme
    context_object_name = "meme"
    template_name = "memes/meme_view.html"

    def get_context_data(self, **kwargs):
        user = get_user(self.request)
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["meme"].karma_given = context["meme"].is_karma_given(user)
        else:
            context["meme"].karma_given = False
        context["form"] = MemeCommentForm()
        return context


class MemeAdd(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {"form": MemeForm()}
        return render(request, "memes/meme_add_view.html", context)   

    def post(self, request):
        if request.user.is_authenticated:
            form = MemeForm(request.POST, request.FILES)
            # TODO: message about failing meme add
            if form.is_valid():
                new_meme = form.save(commit=False)
                new_meme.original_poster = get_user(request)
                new_meme.save()
                return redirect("meme_view", pk=new_meme.pk)
        return redirect("index")


def karma_change(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = get_user(request)
            meme = get_object_or_404(Meme, pk=pk)
            try:
                given_karma = MemeKarma.objects.get(user=user, meme=meme)
                given_karma.delete()
                meme.karma -= 1   
                meme.save()
                msg =  "Successfully taken karma away!"
                karma_given = False
            except MemeKarma.DoesNotExist:
                # meme wasn't given karma point by user
                given_karma = MemeKarma(user=user, meme=meme)
                given_karma.save()
                meme.karma += 1
                meme.save()
                msg = "Successfully given karma point"
                karma_given = True

            return JsonResponse({"success": True, "karma_given": karma_given, "karma": meme.karma, "msg": msg})
        else:
            return JsonResponse({"success": False, "msg": "Log in to vote!"})
    else:
        raise Http404()


def visibility_change(request, pk) -> JsonResponse:
    """Change meme visibility (only available for admin)"""
    if request.method == "POST":
        if request.user.is_authenticated and request.user.is_superuser:
            meme = get_object_or_404(Meme, pk=pk)

            meme.hidden = not meme.hidden
            meme.save()

            # return redirect(reverse("meme_view", args=(meme.pk,)))
            msg = "Successfully set meme visible" if meme.hidden else "Successfully hidden meme"
            return JsonResponse({"success": True, "hidden": meme.hidden, "msg": msg})
        else:
            # return redirect("index")
            return JsonResponse({"success": False, "msg": "No permission!"})
    else:
        raise Http404()


def acceptance_change(request, pk) -> JsonResponse:
    """Change if meme is accepted(visible on main meme listview), available only for admin"""
    if request.method == "POST":
        if request.user.is_authenticated and request.user.is_superuser:
            meme = get_object_or_404(Meme, pk=pk)

            if not meme.accepted:
                meme.accepted = True
                meme.date_accepted = timezone.now()
                meme.save()
                msg = "Successfully accepted meme"
            else:
                meme.accepted = False
                meme.date_accepted = None
                meme.save()
                msg = "Successfully reversed meme acceptance"
            
            return JsonResponse({"success": True, "accepted": meme.accepted, "msg": msg})
            # return redirect(reverse("meme_view", args=(meme.pk,)))
        else:
            # return JsonResponse({"success": False, "msg": "Failed to change acceptance"})
            return JsonResponse({"success": False, "msg": "No permission!"})
            # return redirect("index")
    else:
        raise Http404()
