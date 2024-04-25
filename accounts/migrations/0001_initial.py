from django.db import migrations, models
import django.db.models.deletion

def add_account_and_transaction_data(apps, schema_editor):
    Account = apps.get_model('accounts', 'Account')
    Transaction = apps.get_model('accounts', 'Transaction')
    
    # Create an account with a numeric value (assuming purpose, e.g., score or calculation)
    account = Account.objects.create(account_number='100000000000014', current_balance=100000.00, user=123.00)

    # Create a transaction linked to the account
    Transaction.objects.create(date='2024-01-10', transaction_type='CREDIT', note='Initial credit', amount=100.00, account=account)
    Transaction.objects.create(date='2024-03-10', transaction_type='DEBIT', note='Initial credit', amount=200.00, account=account)
    Transaction.objects.create(date='2024-05-12', transaction_type='CREDIT', note='Initial credit', amount=700.00, account=account)

class Migration(migrations.Migration):

    initial = True

    dependencies = [
          # Adjust based on actual initial migration dependency
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=16, unique=True)),
                ('current_balance', models.DecimalField(decimal_places=2, max_digits=14)),
                ('user', models.DecimalField(decimal_places=2, max_digits=14)),  # Renamed for clarity
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('transaction_type', models.CharField(choices=[('CREDIT', 'Credit'), ('DEBIT', 'Debit')], max_length=6)),
                ('note', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('account', models.ForeignKey(on_delete=models.CASCADE, related_name='transactions', to='accounts.account')),
            ],
        ),
        migrations.RunPython(add_account_and_transaction_data),
    ]
