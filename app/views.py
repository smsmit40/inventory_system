from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Product
from django.db.models import Sum
from .forms import TransactionForm, CreateProductForm


# Create your views here.
def index(request):
    if request.method == 'GET':
        transactions = Product.objects.annotate(product_total=Sum('transaction__total'))
        all_transactions = Transaction.objects.all()
        return render(request, 'app/index.html', {'transactions': transactions, 'all_transactions': all_transactions,
                                                  'form': TransactionForm})
    if 'add_transaction' in request.POST:
        try:
            form=TransactionForm(request.POST)
            new_transaction = form.save(commit=False)
            tolerance=Product.objects.annotate(the_total=Sum('transaction__total')).get(productid=request.POST['product'])
            if type(tolerance.the_total) is None:
                tolerance.the_total = 0
            # entry= the_product.annotate(the_total=Sum('total'))
            # if len(entry) > 0:
            #     tolerance=entry[0]

            if request.POST['transacton_type'] == 'Buy':
                new_transaction.save()
                return redirect('index')
            elif request.POST['transacton_type'] == 'Sell' and int(request.POST['amount']) > int(tolerance.the_total):
                transactions = Product.objects.annotate(product_total=Sum('transaction__total'))
                all_transactions = Transaction.objects.all()
                return render(request, 'app/index.html',
                              {'form': TransactionForm(), 'error':'Inventory cannot go below zero', 'transactions':
                                  transactions, 'all_transactions': all_transactions})
            elif request.POST['transacton_type'] == 'Sell' and int(request.POST['amount']) <= int(tolerance.the_total):
                new_transaction.save()
                return redirect('index')
            else:
                return redirect('index')
        except ValueError as e:
            print(e)
            return render(request, 'app/index.html', {'form': TransactionForm(), 'error': 'bad data passed in'})


def create_product(request):
    if 'create_product' in request.POST:
        return render(request, 'app/create_product.html', {'form': CreateProductForm})

    elif "submit_prod" in request.POST:
        try:
            form = CreateProductForm(request.POST)
            newprod= form.save(commit=False)
            newprod.save()
            return redirect('index')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': CreateProductForm(), 'error': 'bad data passed in'})
    else:
        return render(request, 'app/create_product.html', {'form': CreateProductForm})

def transaction_detail(request, pk):
    detail= get_object_or_404(Transaction, pk=pk)
    obj=Transaction.objects.get(pk=pk)
    new_tol = Product.objects.annotate(the_total=Sum('transaction__total')).get(productname=obj.product)
    if type(new_tol.the_total) is None:
        new_tol.the_total=0
    if request.method == 'GET':
        form = TransactionForm(instance=detail)
        return render(request, 'app/transactiondetail.html', {'form': form, 'detail': detail})

    if 'delete_transaction' in request.POST:
        detail.delete()
        return redirect('index')
    if 'update_transaction' in request.POST:
        try:
            form = TransactionForm(request.POST, instance=detail)
            if request.POST['transacton_type'] == 'Sell' and int(request.POST['amount']) <= int(new_tol.the_total):
                form.save()
                return redirect('index')
            if request.POST['transacton_type'] == 'Sell' and \
                        int(request.POST['amount']) > int(new_tol.the_total):
                error="Inventory cannot drop below zero."
                return render(request, 'app/productdetail.html', {'error': error, 'form': form})
            else:
                form.save()
                return redirect('index')
        except ValueError:
            return render(request, 'app/transactiondetail.html', {'form': form, 'detail': detail, 'error':
                'invalid data in form.'})

def product_detail(request, pk):
    detail = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = CreateProductForm(instance=detail)
        return render(request, 'app/productdetail.html', {'form': form, 'detail': detail})







