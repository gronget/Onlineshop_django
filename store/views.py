from django.shortcuts import render,HttpResponse,get_object_or_404
from category.models import Category
from .models import Product
from django.db.models import Q
from cart.models import CartItem
from cart.views import _cart_id

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None
    print(f" ---sesion in store get {request.session.session_key} ")
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        # print(f"----{dir(request.GET)} ")
        print(f"----{request.GET.get} ")
        paged_products = paginator.get_page(page)
        product_count = products.count()
        # print(f"---- {[x.images.url for x in paged_products]}")
        # print(f"-----{type(paged_products)}")
        # print(f"-----{dir(paged_products)}")
        # print(f"-----{paged_products.object_list}")
        

        

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

###vUBJePia87KUqf4ogBi9l6HVZTwkzkOkDAyCh1ZIcjHkcGy2pK0Vu3YBCTpPEvWz
def product_detail(request, category_slug, product_slug):
    print(f" ---sesion in product get {request.session.session_key} ")
    try:
        single_product = Product.objects.get(category__slug=category_slug ,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }

    return render(request, 'store/product_detail.html', context)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)
