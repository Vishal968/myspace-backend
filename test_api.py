from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

# from data import connect, disconnect, execute, helper_upload_img, helper_icon_img
from data_pm import connect, uploadImage, s3
import boto3
import json
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import pymysql
import datetime
import json
from decimal import Decimal
import requests
import pytest

ENDPOINT = "https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev"

def test_get_dashboard():
    response_m = requests.get(ENDPOINT + "/dashboard/600-000038")
    response_o = requests.get(ENDPOINT + "/dashboard/110-000099")
    response_t = requests.get(ENDPOINT + "/dashboard/350-000068")
    response_mt = requests.get(ENDPOINT + "/dashboard/600-000039")

    assert response_m.status_code == 200
    assert response_o.status_code == 200
    assert response_t.status_code == 200
    assert response_mt.status_code == 200

def test_get_cashflow():
    response = requests.get(ENDPOINT + "/cashflowByOwner/110-000099/TTM")

    assert response.status_code == 200

def test_get_payment_status():
    response = requests.get(ENDPOINT + "/paymentStatus/600-000038")

    assert response.status_code == 200

def test_get_allTransactions():
    response = requests.get(ENDPOINT + "/allTransactions")

    assert response.status_code == 200

def test_get_properties():
    response = requests.get(ENDPOINT + "/properties/110-000099")

    assert response.status_code == 200

def test_get_listings():
    response = requests.get(ENDPOINT + "/listings")

    assert response.status_code == 200

def test_get_properties_by_manager():
    response = requests.get(ENDPOINT + "/propertiesByManager/110-000099/600-000038")

    assert response.status_code == 200

def test_get_contracts():
    response = requests.get(ENDPOINT + "/contracts/110-000099")

    assert response.status_code == 200

def test_get_rents():
    response = requests.get(ENDPOINT + "/rents/110-000099")

    assert response.status_code == 200


def test_get_maintenance_by_property():
    response = requests.get(ENDPOINT + "/maintenanceByProperty/200-000084")

    assert response.status_code == 200

def test_get_maintenanceReq():
    response = requests.get(ENDPOINT + "/maintenanceReq/110-000099")

    assert response.status_code == 200

def test_get_maintenanceStatus():
    response = requests.get(ENDPOINT + "/maintenanceStatus/600-000038")

    assert response.status_code == 200

def test_get_searchManager():
    response = requests.get(ENDPOINT + "/searchManager?")

    assert response.status_code == 200

def test_get_leaseDetails():
    response = requests.get(ENDPOINT + "/leaseDetails/600-000038")

    assert response.status_code == 200

def test_get_announcements():
    response = requests.get(ENDPOINT + "/announcements/110-000099")

    assert response.status_code == 200

def test_get_contacts():
    response = requests.get(ENDPOINT + "/contacts/600-000038")

    assert response.status_code == 200

def test_get_contactsMaintenance():
    response = requests.get(ENDPOINT + "/contactsMaintenance")

    assert response.status_code == 200

def test_get_businessProfile():
    response = requests.get(ENDPOINT + "/businessProfile/600-000038")

    assert response.status_code == 200

def test_get_ownerProfile():
    response = requests.get(ENDPOINT + "/ownerProfile/110-000099")

    assert response.status_code == 200

def test_get_tenantProfile():
    response = requests.get(ENDPOINT + "/tenantProfile/350-000068")

    assert response.status_code == 200

def test_get_ownerDocuments():
    response = requests.get(ENDPOINT + "/ownerDocuments/110-000099")

    assert response.status_code == 200

def test_put_properties():
    payload = {'property_uid': '200-000084', 'property_address': 'Bellevue Square 2302', 'property_unit': '2', 'property_city': 'Seattle', 'property_state': 'CA', 'property_zip': '97324', 'property_type': 'Single Family', 'property_num_beds': '0', 'property_num_baths': '2', 'property_area': '0', 'property_listed_rent': '0', 'property_deposit': '0', 'property_pets_allowed': '0', 'property_deposit_for_rent': '0', 'property_taxes': '0', 'property_mortgages': '0', 'property_insurance': '0', 'property_featured': '0', 'property_description': 'test', 'property_notes': '', 'property_available_to_rent': ''}
    response = requests.put(ENDPOINT + "/properties", data=payload)

    assert response.status_code == 200
    data = response.json()
    print(data)

def test_post_addExpense():
    payload = {"pur_property_id":"200-000088","purchase_type":"Insurance","pur_cf_type":"expense","purchase_date":"2023-10-16","pur_due_date":"2023-10-16","pur_amount_due":323232,"purchase_status":"COMPLETED","pur_notes":"This is just a note","pur_description":"hi","pur_receiver":"110-000099","pur_initiator":"110-000099","pur_payer": ''}
    response = requests.post(ENDPOINT + "/addExpense", json = payload)

    assert response.status_code == 200
    data = response.json()
    print(data)

def test_PM_Tenant_Flow():

    tenant_id = '350-000068'
    property_id = '200-000084'

    payload = {'property_uid': '200-000084', 'property_available_to_rent': '1', 'property_active_date': '2023-11-06', 'property_address': 'Bellevue Square 2302', 'property_unit': '2', 'property_city': 'Seattle', 'property_state': 'CA', 'property_zip': '97324', 'property_type': 'Single Family', 'property_num_beds': '0', 'property_num_baths': '2', 'property_area': '0', 'property_listed_rent': '0', 'property_deposit': '0', 'property_pets_allowed': '0', 'property_deposit_for_rent': '0', 'property_taxes': '0', 'property_mortgages': '0', 'property_insurance': '0', 'property_featured': '0', 'property_description': '', 'property_notes': ''}
    response = requests.put(ENDPOINT + "/properties", data=payload)

    assert response.status_code == 200


    response = requests.get(ENDPOINT + "/listings")

    assert response.status_code == 200

    response = requests.get(ENDPOINT + "/leaseDetails/350-000068")

    assert response.status_code == 200

    payload = {"announcement_title":"New Tenant Application","announcement_msg":"You have a new tenant application for your property","announcement_sender":"350-000068","announcement_date":"Mon Nov 06 2023","announcement_properties":"200-000084","announcement_mode":"LEASE","announcement_receiver":"600-000038","announcement_type":["App"]}

    response = requests.post(ENDPOINT + "/announcements/350-000068", json=payload)

    assert response.status_code == 200

    payload = {"lease_property_id":"200-000084","lease_status":"NEW","lease_assigned_contacts":"[\"350-000068\"]","lease_documents":"[]","lease_adults":"[]","lease_children":"[]","lease_pets":"[]","lease_vehicles":"[]","lease_referred":"[]","lease_rent":"[]","lease_application_date":"11/6/2023","tenant_uid":"350-000068"}

    response = requests.post(ENDPOINT + "/leaseApplication", data = payload)

    data = response.json()

    print(data)

    assert response.status_code == 200

    response = requests.get(ENDPOINT + "/contracts/600-000038")

    assert response.status_code == 200

    response = {}
    with connect() as db:
        leaseQuery = db.execute("""
                        SELECT lease_uid from space.leases
                        LEFT JOIN space.lease_tenant ON lt_lease_id = lease_uid
                        WHERE lt_tenant_id = \'""" + tenant_id + """\' AND lease_property_id = \'""" + property_id + """\';
                                        """)

        # print("Query: ", propertiesQuery)
        response["lease"] = leaseQuery

        lease_uid = response['lease']['result'][0]['lease_uid']

    payload = {"lease_uid": lease_uid,"lease_status":"PROCESSING","lease_start":"11/6/2023","lease_end":"11/5/2024","lease_fees":[{"id":1,"fee_name":"rent","fee_type":"$","frequency":"Monthly","charge":"300","due_by":"1st","late_by":"2","late_fee":"200","perDay_late_fee":"20","available_topay":""}]}

    response = requests.put(ENDPOINT + "/leaseApplication", json = payload)

    assert response.status_code == 200

    payload = {"announcement_title":"New Lease created","announcement_msg":"You have a new lease to be approved for your property","announcement_sender":"600-000038","announcement_date":"Mon Nov 06 2023","announcement_properties":"200-000084","announcement_mode":"LEASE","announcement_receiver":"350-000068","announcement_type":["App"]}

    response = requests.post(ENDPOINT + "/announcements/600-000038", json=payload)

    assert response.status_code == 200

    payload = {"lease_uid":lease_uid,"lease_status":"ACTIVE"}

    response = requests.put(ENDPOINT + "/leaseApplication", json=payload)

    assert response.status_code == 200

    response = {}
    with connect() as db:

        leaseQuery = ("""
                DELETE space.leases
                FROM space.leases
                LEFT JOIN space.lease_tenant ON lt_lease_id = lease_uid
                WHERE lease_uid = \'""" + lease_uid + """\';
                """)

        response["delete_lease"] = db.delete(leaseQuery)


        leaseQuery = ("""
                DELETE space.lease_tenant
                FROM space.lease_tenant
                WHERE lt_lease_id = \'""" + lease_uid + """\';
                """)

        response["delete_lease_tenant"] = db.delete(leaseQuery)

    print(response)

def test_PM_Owner():

    payload = {'property_owner_id': ['110-000099'], 'property_available_to_rent': ['0'], 'property_active_date': ['2023-11-07'], 'property_address': ['253rd Arizona'], 'property_unit': ['2'], 'property_city': ['Tucson'], 'property_state': ['AZ'], 'property_zip': ['80000'], 'property_type': ['Condo'], 'property_num_beds': ['2'], 'property_num_baths': ['3'], 'property_value': ['200000'], 'property_area': ['2323'], 'property_listed': ['0'], 'property_deposit': ['0'], 'property_pets_allowed': ['0'], 'property_deposit_for_rent': ['0'], 'property_taxes': ['0'], 'property_mortgages': ['0'], 'property_insurance': ['0'], 'property_featured': ['0'], 'property_description': [''], 'property_notes': ['test'], 'img_cover': ['']}

    response = requests.post(ENDPOINT + "/properties", data = payload)

    assert response.status_code == 200

    response1 = {}
    response2 = {}
    with connect() as db:
        propertyQuery = db.execute("""
                                SELECT property_uid from space.properties
                                LEFT JOIN space.property_owner ON property_uid = property_id
                                WHERE property_owner_id = '110-000099' AND property_address = '253rd Arizona';
                                                """)

        # print("Query: ", propertiesQuery)
        response1["property"] = propertyQuery

        property_uid = response1['property']['result'][0]['property_uid']



    payload = {"announcement_title":"black","announcement_msg":"hello","announcement_sender":"110-000099","announcement_date":"2023-11-07","announcement_properties":["200-000147"],"announcement_mode":"CONTRACT","announcement_receiver":["600-000038"],"announcement_type":["App"]}

    response = requests.post(ENDPOINT + "/announcements/110-000099", json=payload)

    assert response.status_code == 200

    payload = {'contract_property_id':property_uid,'contract_business_id': '600-000038','contract_start_date':'2023-11-07',
    'contract_status': 'NEW'}

    response = requests.post(ENDPOINT + "/contracts", data=payload)

    assert response.status_code == 200

    with connect() as db:
        contractQuery = db.execute("""
                                        SELECT contract_uid from space.contracts
                                        WHERE contract_property_id = \'""" + property_uid + """\' AND contract_business_id = '600-000038';
                """)

        response2["contract"] = contractQuery

        contract_uid = response2['contract']['result'][0]['contract_uid']

    payload = {'contract_uid': contract_uid, 'contract_name': 'Black ', 'contract_start_date': '2023-11-07', 'contract_end_date': '12-12-2023', 'contract_fees': '[{"fee_name":"Black","fee_type":"FLAT-RATE","frequency":"One Time","isPercentage":false,"isFlatRate":true,"charge":"1000"}]', 'contract_status': 'SENT', 'contract_assigned_contacts': '[]'}

    response = requests.put(ENDPOINT + "/contracts", data=payload)

    assert response.status_code == 200

    payload = {'contract_uid': contract_uid, 'contract_status': 'ACTIVE'}

    response = requests.put(ENDPOINT + "/contracts", data=payload)

    assert response.status_code == 200

    response = {}

    with connect() as db:
        propertyQuery = db.execute("""
                        SELECT property_uid from space.properties
                        LEFT JOIN space.property_owner ON property_uid = property_id
                        WHERE property_owner_id = '110-000099' AND property_address = '253rd Arizona';
                                        """)

        # print("Query: ", propertiesQuery)
        response["property"] = propertyQuery

        for i in range(len(response['property']['result'])):
            property_uid = response['property']['result'][i]['property_uid']
            delQuery = ("""
                        DELETE from space.properties WHERE property_uid = \'""" + property_uid + """\';
            """)
            delQuery2 = ("""
                        DELETE from space.property_owner WHERE property_id = \'""" + property_uid + """\';
            """)

            response[i] = db.delete(delQuery)
            response2[i] = db.delete(delQuery2)

        contractQuery = ("""
                        DELETE from space.contracts WHERE contract_uid = \'""" + contract_uid + """\';
        """)

        response3 = db.delete(contractQuery)

    print(response, response2, response3)

def test_Maintenance_flow():
# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/maintenanceRequests
# Request Method:
# POST

    payload = {'maintenance_property_id': '200-000084', 'maintenance_title': 'Vents Broken', 'maintenance_desc': 'Vents ', 'maintenance_request_type': 'Appliance', 'maintenance_request_created_by': '600-000038', 'maintenance_priority': 'High', 'maintenance_can_reschedule': '1', 'maintenance_assigned_business': 'null', 'maintenance_assigned_worker': 'null', 'maintenance_scheduled_date': 'null', 'maintenance_scheduled_time': 'null', 'maintenance_frequency': 'One Time', 'maintenance_notes': 'null', 'maintenance_request_created_date': '2023-11-13', 'maintenance_request_closed_date': 'null', 'maintenance_request_adjustment_date': 'null'}

    response = requests.post(ENDPOINT + "/maintenanceRequests", data = payload)

    assert response.status_code == 200

    response = {}
    with connect() as db:
        maintenanceQuery = db.execute("""
                                        SELECT maintenance_request_uid from space.maintenanceRequests
                                        WHERE maintenance_property_id = '200-000084' AND maintenance_title = 'Vents Broken';
                """)

        response["maint"] = maintenanceQuery

        maintenance_request_uid = response['maint']['result'][0]['maintenance_request_uid']

# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/quotes
# Request Method:
# POST
    payload = {'quote_maintenance_request_id': maintenance_request_uid, 'quote_pm_notes': 'Vents', 'quote_maintenance_contacts': '600-000039'}

    response = requests.post(ENDPOINT + "/quotes", data = payload)

    assert response.status_code == 200
# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/maintenanceRequests
# Request Method:
# PUT
    with connect() as db:
        response = {}
        quoteQuery = db.execute("""
                                    SELECT maintenance_quote_uid from space.maintenanceQuotes
                                    WHERE quote_maintenance_request_id = \'""" + maintenance_request_uid + """\';
                """)

        response["quote"] = quoteQuery

        maintenance_quote_uid = response['quote']['result'][0]['maintenance_quote_uid']

    payload = {"maintenance_request_uid":maintenance_request_uid,"maintenance_request_status":"PROCESSING"}

    response = requests.put(ENDPOINT + "/maintenanceRequests", json = payload)
    assert response.status_code == 200
# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/maintenanceQuotes
# Request Method:
# PUT
    payload = {'maintenance_quote_uid': maintenance_quote_uid, 'quote_maintenance_request_id': '800-000180', 'quote_business_id': '600-000039', 'quote_services_expenses': '{"per Hour Charge":"10","event_type":5,"service_name":"Labor","parts":[{"part":"250","quantity":"1","cost":"250"}],"labor":[{"description":"","hours":5,"rate":"10"}],"total_estimate":50}', 'quote_notes': 'vents', 'quote_status': 'SENT', 'quote_event_type': '5 Hour Job', 'quote_total_estimate': '300', 'quote_created_date': '2000-04-23 00:00:00', 'quote_earliest_availability': '2023-12-12 12:12:12'}

    response = requests.put(ENDPOINT + "/maintenanceQuotes", data = payload)

    assert response.status_code == 200
# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/maintenanceQuotes
# Request Method:
# PUT
    payload = {'maintenance_quote_uid': maintenance_quote_uid, 'quote_status': 'ACCEPTED'}

    response = requests.put(ENDPOINT + "/maintenanceQuotes", data = payload)

    assert response.status_code == 200
# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/maintenanceRequests
# Request Method:
# PUT
    payload = {"maintenance_request_uid":maintenance_request_uid,"maintenance_request_status":"SCHEDULED","maintenance_scheduled_date":"10/30/2023","maintenance_scheduled_time":"10:00:00"}

    response = requests.put(ENDPOINT + "/maintenanceRequests", json = payload)

    assert response.status_code == 200
# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/maintenanceQuotes
# Request Method:
# PUT
    payload = {'maintenance_quote_uid': maintenance_quote_uid, 'quote_status': 'SCHEDULED'}

    response = requests.put(ENDPOINT + "/maintenanceQuotes", data = payload)

    assert response.status_code == 200
# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/maintenanceRequests
# Request Method:
# PUT
    payload = {"maintenance_request_uid":maintenance_request_uid,"maintenance_request_status":"COMPLETED"}

    response = requests.put(ENDPOINT + "/maintenanceRequests", json=payload)

    assert response.status_code == 200
# Request URL:
# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/maintenanceQuotes
# Request Method:
# PUT
    payload = {'maintenance_quote_uid': maintenance_quote_uid,'quote_status': 'FINISHED'}

    response = requests.put(ENDPOINT + "/maintenanceQuotes", data=payload)

    assert response.status_code == 200
# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/maintenanceRequests
# Request Method:
# PUT
    payload = {"maintenance_request_uid":maintenance_request_uid,"maintenance_request_status":"PAID"}

    response = requests.put(ENDPOINT + "/maintenanceRequests", json=payload)

    assert response.status_code == 200
# Request URL:
# https://l0h6a9zi1e.execute-api.us-west-1.amazonaws.com/dev/maintenanceQuotes
# Request Method:
# PUT

    payload = {'maintenance_quote_uid': maintenance_quote_uid,'quote_status': 'COMPLETED'}

    response = requests.put(ENDPOINT + "/maintenanceQuotes", data=payload)

    assert response.status_code == 200

    response = {}
    response1 = {}
    with connect() as db:
        delQuery = ("""
                            DELETE space.maintenanceRequests
                            FROM space.maintenanceRequests
                            WHERE maintenance_request_uid = \'""" + maintenance_request_uid + """\';
                            """)


        response["delete_req"] = db.delete(delQuery)

        delQuery = ("""
                                    DELETE space.maintenanceQuotes
                                    FROM space.maintenanceQuotes
                                    WHERE maintenance_quote_uid = \'""" + maintenance_quote_uid + """\';
                                    """)

        response1["delete_quote"] = db.delete(delQuery)

    print(response)
    print(response1)
