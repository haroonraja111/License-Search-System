from django.db import models

class License(models.Model):
    serialno = models.BigAutoField(db_column='SerialNo', primary_key=True)  # Field name made lowercase.
    computerno = models.BigIntegerField(db_column='ComputerNo', blank=True, null=True)  # Field name made lowercase.
    licenseno = models.CharField(db_column='LicenseNo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    learnerno = models.CharField(db_column='LearnerNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    learnerdate = models.DateTimeField(db_column='LearnerDate', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fathername = models.CharField(db_column='FatherName', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dob = models.DateTimeField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.
    issuedate = models.DateTimeField(db_column='IssueDate', blank=True, null=True)  # Field name made lowercase.
    expirydate = models.DateTimeField(db_column='ExpiryDate', blank=True, null=True)  # Field name made lowercase.
    rnewexpirydate = models.DateTimeField(db_column='RNewExpiryDate', blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cnic = models.CharField(db_column='CNIC', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # bloodgroup = models.CharField(db_column='BloodGroup', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    amount = models.CharField(db_column='Amount', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    enterby = models.CharField(db_column='EnterBy', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # enteron = models.CharField(db_column='EnterOn', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # isprint = models.SmallIntegerField(db_column='IsPrint', blank=True, null=True)  # Field name made lowercase.
    # islpc = models.SmallIntegerField(db_column='IsLPC', blank=True, null=True)  # Field name made lowercase.
    # isoldlp = models.SmallIntegerField(db_column='IsOldLP', blank=True, null=True)  # Field name made lowercase.
    # isndl = models.SmallIntegerField(db_column='IsNDL', blank=True, null=True)  # Field name made lowercase.
    mobileno = models.CharField(db_column='MobileNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # owner = models.CharField(db_column='Owner', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # relationship = models.CharField(db_column='Relationship', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    verified = models.SmallIntegerField(db_column='Verified', blank=True, null=True)  # Field name made lowercase.
    verifiedby = models.CharField(db_column='VerifiedBy', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    verifieddate = models.DateTimeField(db_column='VerifiedDate', blank=True, null=True)  # Field name made lowercase.
    enable = models.SmallIntegerField(db_column='Enable', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'License'

    def __str__(self):
        return f"{self.name} - {self.licenseno}"

class Endorsenumber(models.Model):
    serialno = models.BigAutoField(db_column='SerialNo', primary_key=True)  # Field name made lowercase.
    number = models.BigIntegerField(db_column='Number', blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EndorseNumber'

    def __str__(self):
        return str(self.number)

class Updationtype(models.Model):
    updationtypeno = models.BigAutoField(db_column='UpdationTypeNo', primary_key=True)  # Primary Key
    description = models.CharField(db_column='Description', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'UpdationType'

    def __str__(self):
        return self.description

class Licenseupdation(models.Model):
    serialno = models.BigAutoField(db_column='SerialNo', primary_key=True)
    computerno = models.CharField(db_column='ComputerNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    number = models.CharField(db_column='Number', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    updationtypeno = models.ForeignKey(
        Updationtype,
        on_delete=models.CASCADE,
        db_column='UpdationTypeNo',
        related_name='license_updations'
    )
    preexpiry = models.DateTimeField(db_column='PreExpiry')
    newissuedate = models.DateTimeField(db_column='NewIssueDate')
    newexpirydate = models.DateTimeField(db_column='NewExpiryDate')
    amountpaid = models.CharField(db_column='AmountPaid', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    enterby = models.CharField(db_column='EnterBy', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    enteron = models.CharField(db_column='EnterOn', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    status = models.CharField(db_column='Status', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    type = models.CharField(db_column='Type', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LicenseUpdation'

    def __str__(self):
        return f"{self.number} - {self.updationtypeno.description}"

class Vehicletype(models.Model):
    vehicletypeid = models.IntegerField(db_column='VehicleTypeID', primary_key=True)  # Set as primary key for FK reference
    description = models.CharField(db_column='Description', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VehicleType'

    def __str__(self):
        return self.description

class Licensevehicle(models.Model):
    licenseno = models.CharField(db_column='LicenseNo', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    vehicletype = models.ForeignKey(
        Vehicletype,
        db_column='VehicleTypeID',
        on_delete=models.CASCADE,
        to_field='vehicletypeid',
        related_name='license_vehicles'
    )
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LicenseVehicle'
        unique_together = (('licenseno', 'vehicletype'),)

    def __str__(self):
        return f"{self.licenseno} - {self.vehicletype.vehicletypeid if self.vehicletype else 'None'}"
