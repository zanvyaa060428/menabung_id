from django.urls import path
from . import views


urlpatterns = [


path(
        "admin/guru/",
        views.data_guru,
        name="data_guru"
    ),

    path(
        "admin/guru/tambah/",
        views.tambah_guru,
        name="tambah_guru"
    ),

    path(
        "admin/guru/<int:id>/edit/",
        views.edit_guru,
        name="edit_guru"
    ),

    path(
        "admin/guru/<int:id>/hapus/",
        views.hapus_guru,
        name="hapus_guru"
    ),


    # LOGIN
    path(
        "",
        views.login_view,
        name="login"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),


    # ADMIN
    path(
        "admin/dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "admin/siswa/",
        views.data_siswa,
        name="data_siswa"
    ),
  path(
    "admin/siswa/tambah/",
    views.tambah_siswa,
    name="tambah_siswa"
),

path(
    "admin/siswa/<int:id>/edit/",
    views.edit_siswa,
    name="edit_siswa"
),

  path(
    "admin/siswa/<int:id>/hapus/",
    views.hapus_siswa,
    name="hapus_siswa"
),
  
    path(
        "admin/siswa/<int:id>/",
        views.detail_siswa,
        name="detail_siswa"
    ),

  # TRANSAKSI
path(
    "admin/transaksi/",
    views.transaksi,
    name="transaksi"
),

  # RIWAYAT TRANSAKSI
path(
    "admin/riwayat-transaksi/",
    views.riwayat_transaksi,
    name="riwayat_transaksi"
),

  path(
    "admin/laporan/",
    views.laporan,
    name="laporan"
),

  path(
    "siswa/riwayat/",
    views.riwayat_siswa,
    name="riwayat_siswa"
),

    # GURU
    path(
        "guru/dashboard/",
        views.guru_dashboard,
        name="guru_dashboard"
    ),


    # SISWA

path(
    "siswa/dashboard/",
    views.siswa_dashboard,
    name="siswa_dashboard"
),


path(
    "siswa/pengumuman/",
    views.pengumuman_siswa,
    name="pengumuman_siswa"
),

path(
    "siswa/riwayat/",
    views.riwayat_siswa,
    name="riwayat_siswa"
),


    # LOGOUT
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

path("admin/kelas/", views.data_kelas, name="data_kelas"),

path(
    "admin/kelas/tambah/",
    views.tambah_kelas,
    name="tambah_kelas"
),

path(
    "admin/kelas/<int:id>/edit/",
    views.edit_kelas,
    name="edit_kelas"
),

path(
    "admin/kelas/<int:id>/hapus/",
    views.hapus_kelas,
    name="hapus_kelas"
),

path(
    "admin/pengumuman/",
    views.data_pengumuman,
    name="data_pengumuman"
),

  path(
    "admin/pengumuman/tambah/",
    views.tambah_pengumuman,
    name="tambah_pengumuman"
),
  
]