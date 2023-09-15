from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection
from .forms import PollingUnitResultForm
from django.db import connection
from django.utils import timezone
import os
from .utils import get_client_ip
from django.contrib import messages

def polling_unit_result(request, unique_id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM announced_pu_results WHERE polling_unit_uniqueid = %s"
        cursor.execute(sql, (unique_id,))
        results = cursor.fetchall()

    # Render a template to display the results
    context = {'results': results}
    return render(request, 'polling_unit_result.html', context)

def local_government_result(request):
    # Fetch the list of local governments from the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT uniqueid, polling_unit_name FROM polling_unit")
        local_governments = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]

    total_results = {}
    if request.method == 'POST':
        selected_lga_id = request.POST['selected_lga']

        # Calculate the summed total result for the selected local government
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT party_abbreviation, SUM(party_score) "
                "FROM announced_pu_results AS pu "
                "JOIN polling_unit AS pu_unit ON pu.polling_unit_uniqueid = pu_unit.uniqueid "
                "WHERE pu_unit.uniqueid = %s "
                "GROUP BY party_abbreviation",
                [selected_lga_id]
            )
            total_results = dict(cursor.fetchall())

    context = {
        'local_governments': local_governments, 
        'total_results': total_results
    }
    return render(request, 'local_government_result.html', context)

def add_polling_unit_result(request):
    if request.method == 'POST':
        form = PollingUnitResultForm(request.POST)
        if form.is_valid():
            # Get the cleaned data from the form
            cleaned_data = form.cleaned_data

            # Extract party scores from cleaned_data
            party_scores = {
                'PDP': cleaned_data['pdp_score'],
                'DPP': cleaned_data['dpp_score'],
                'ACN': cleaned_data['acn_score'],
                'PPA': cleaned_data['ppa_score'],
                'CDC': cleaned_data['cdc_score'],
                'JP': cleaned_data['jp_score'],
                # Add more party scores as needed
            }

            # Save the results in the database using raw SQL queries or Django models
            with connection.cursor() as cursor:
                for party, score in party_scores.items():
                    cursor.execute(
                        "INSERT INTO announced_pu_results "
                        "(polling_unit_uniqueid, party_abbreviation, party_score, entered_by_user, date_entered, user_ip_address) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        [
                            cleaned_data['polling_unit_unique_id'],
                            party,
                            score,
                            'Ifeanyi Onyekwelu',
                            timezone.now(),
                            get_client_ip(request),
                        ]
                    )

            messages.success(request, 'Polling unit result saved successfully')
            return redirect('election_results_app:polling_unit_result', unique_id=cleaned_data['polling_unit_unique_id'])
    else:
        form = PollingUnitResultForm()

    context = {
        'form': form,
    }
    return render(request, 'polling_unit_result_form.html', context)
