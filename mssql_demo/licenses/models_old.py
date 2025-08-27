from django.db import models




class OldLicense(models.Model):
    serialno = models.BigAutoField(db_column='SerialNo', primary_key=True)
    computerno = models.BigIntegerField(db_column='ComputerNo', blank=True, null=True)
    licenseno = models.CharField(db_column='LicenseNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fathername = models.CharField(db_column='FatherName', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dob = models.CharField(db_column='DOB', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    learnerno = models.CharField(db_column='LearnerNo', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    learnerdate = models.CharField(db_column='LearnerDate', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    issuedate = models.CharField(db_column='IssueDate', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    expirydate = models.CharField(db_column='ExpiryDate', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vehicletype = models.CharField(db_column='VehicleType', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    address = models.CharField(db_column='Address', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cnic = models.CharField(db_column='CNIC', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    # bloodgroup = models.CharField(db_column='BloodGroup', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    amount = models.CharField(db_column='Amount', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    version = models.CharField(db_column='Version', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    userid = models.CharField(db_column='UserID', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    comments = models.CharField(db_column='Comments', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    verifieddate = models.CharField(db_column='VerifiedDate', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)
    verifiedby = models.CharField(db_column='VerifiedBy', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    blocked = models.SmallIntegerField(db_column='Blocked', blank=True, null=True)

    class Meta:
        db_table = 'Old_License'


class Dialogbox(models.Model):
    licenseno = models.CharField(db_column='LicenseNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    endo_issue = models.CharField(db_column='Endo_Issue', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS')
    vehicletype = models.CharField(db_column='VehicleType', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS')
    endo_user = models.CharField(db_column='Endo_User', max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS')
    changedate = models.DateTimeField(db_column='ChangeDate', blank=True, null=True)

    class Meta:
        db_table = 'DialogBox'

class Vehicle(models.Model):
    vehicleno = models.BigIntegerField(db_column='VehicleNo', primary_key=True)
    description = models.CharField(db_column='Description', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        db_table = 'Vehicle'


class Endo(models.Model):
    serialno = models.BigAutoField(db_column='SerialNo', primary_key=True)
    licenseno = models.CharField(db_column='LicenseNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    endo_user = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    endo_user1 = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vehicletype = models.CharField(db_column='VehicleType', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    endo_issue = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    endo_exp = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        db_table = 'endo'
