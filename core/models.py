from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10)
    nama = models.CharField(max_length=100)
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'
        managed = False


class Guru(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    nip = models.CharField(max_length=30, unique=True, null=True)
    nama = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    no_hp = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'guru'
        managed = False


class Kelas(models.Model):
    id = models.AutoField(primary_key=True)
    nama_kelas = models.CharField(max_length=50)
    tingkat = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'kelas'
        managed = False


class Siswa(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    kelas_id = models.IntegerField(null=True)
    nis = models.CharField(max_length=30, unique=True, null=True)
    nama = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    no_hp = models.CharField(max_length=20, null=True)
    alamat = models.TextField(null=True)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'siswa'
        managed = False


class Transaksi(models.Model):
    id = models.AutoField(primary_key=True)
    siswa_id = models.IntegerField()
    guru_id = models.IntegerField(null=True)
    jenis = models.CharField(max_length=10)
    nominal = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_sebelum = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_sesudah = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.CharField(max_length=255, null=True)
    tanggal = models.DateTimeField(null=True)

    class Meta:
        db_table = 'transaksi'
        managed = False


class Pengumuman(models.Model):
    id = models.AutoField(primary_key=True)
    judul = models.CharField(max_length=150)
    isi = models.TextField()
    dibuat_oleh = models.IntegerField(null=True)
    tanggal = models.DateTimeField(null=True)

    class Meta:
        db_table = 'pengumuman'
        managed = False


class ActivityLog(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    aktivitas = models.CharField(max_length=255)
    waktu = models.DateTimeField(null=True)

    class Meta:
        db_table = 'activity_logs'
        managed = False