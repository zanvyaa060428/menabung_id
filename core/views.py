from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from functools import wraps
from .models import User, Guru, Siswa, Kelas, Transaksi, Pengumuman

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_id = request.session.get("user_id")
            role = request.session.get("role")

            if not user_id:
                return redirect("login")

            if role not in roles:
                messages.error(request, "Kamu tidak memiliki akses ke halaman ini.")

                if role == "admin":
                    return redirect("admin_dashboard")
                elif role == "guru":
                    return redirect("guru_dashboard")
                elif role == "siswa":
                    return redirect("siswa_dashboard")

                return redirect("login")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator

@role_required("admin")
def data_kelas(request):

    kelas = Kelas.objects.all().order_by("nama_kelas")

    context = {
        "kelas": kelas
    }

    return render(
        request,
        "core/data_kelas.html",
        context
    )

@role_required("admin")
def tambah_kelas(request):

    if request.method == "POST":

        nama_kelas = request.POST.get(
            "nama_kelas",
            ""
        ).strip()

        tingkat = request.POST.get(
            "tingkat",
            ""
        ).strip()

        Kelas.objects.create(
            nama_kelas=nama_kelas,
            tingkat=tingkat
        )

        return redirect("data_kelas")

    return render(
        request,
        "core/tambah_kelas.html"
    )

@role_required("admin")
def edit_kelas(request, id):

    kelas = get_object_or_404(
        Kelas,
        id=id
    )

    if request.method == "POST":

        kelas.id_kelas = request.POST.get(
            "id_kelas",
            ""
        ).strip()

        kelas.nama_kelas = request.POST.get(
            "nama_kelas",
            ""
        ).strip()

        kelas.tingkat = request.POST.get(
            "tingkat",
            ""
        ).strip()

        kelas.wali_kelas = request.POST.get(
            "wali_kelas",
            ""
        ).strip()

        kelas.save()

        return redirect("data_kelas")

    return render(
        request,
        "core/edit_kelas.html",
        {
            "kelas": kelas
        }
    )

@role_required("admin")
def hapus_kelas(request, id):

    kelas = get_object_or_404(
        Kelas,
        id=id
    )

    if request.method == "POST":

        kelas.delete()

        return redirect("data_kelas")

    return render(
        request,
        "core/hapus_kelas.html",
        {
            "kelas": kelas
        }
    )

@role_required("admin")
def data_guru(request):

    guru = Guru.objects.all().order_by("nama")

    keyword = request.GET.get("q", "").strip()

    if keyword:
        guru = guru.filter(
            nama__icontains=keyword
        ) | guru.filter(
            nip__icontains=keyword
        )

    context = {
        "guru": guru,
        "keyword": keyword,
    }

    return render(
        request,
        "core/data_guru.html",
        context
    )

@role_required("admin")
def tambah_guru(request):

    if request.method == "POST":

        nip = request.POST.get("nip", "").strip()
        nama = request.POST.get("nama", "").strip()
        email = request.POST.get("email", "").strip()
        no_hp = request.POST.get("no_hp", "").strip()

        user = User.objects.create(
            username=nip,
            password=nip,
            role="guru",
            nama=nama
        )

        Guru.objects.create(
            user_id=user.id,
            nip=nip,
            nama=nama,
            email=email,
            no_hp=no_hp
        )

        return redirect("data_guru")

    return render(
        request,
        "core/tambah_guru.html"
    )

@role_required("admin")
def edit_guru(request, id):

    guru = get_object_or_404(
        Guru,
        id=id
    )

    if request.method == "POST":

        guru.nip = request.POST.get(
            "nip", ""
        ).strip()

        guru.nama = request.POST.get(
            "nama", ""
        ).strip()

        guru.email = request.POST.get(
            "email", ""
        ).strip()

        guru.no_hp = request.POST.get(
            "no_hp", ""
        ).strip()

        guru.save()

        return redirect("data_guru")

    return render(
        request,
        "core/edit_guru.html",
        {
            "guru": guru
        }
    )

@role_required("admin")
def hapus_guru(request, id):

    guru = get_object_or_404(
        Guru,
        id=id
    )

    if request.method == "POST":

        guru.delete()

        return redirect("data_guru")

    return render(
        request,
        "core/hapus_guru.html",
        {
            "guru": guru
        }
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(
            username=username,
            password=password
        ).first()

        if user:
            request.session["user_id"] = user.id
            request.session["role"] = user.role
            request.session["nama"] = user.nama

            if user.role == "admin":
                return redirect("admin_dashboard")

            elif user.role == "guru":
                return redirect("guru_dashboard")

            elif user.role == "siswa":
                return redirect("siswa_dashboard")

        messages.error(
            request,
            "Username atau password salah."
        )

    return render(request, "core/login.html")


def hapus_kelas(request, id):

    kelas = get_object_or_404(Kelas, id=id)

    if request.method == "POST":

        kelas.delete()

        return redirect("data_kelas")

    return render(
        request,
        "core/hapus_kelas.html",
        {"kelas": kelas}
    )

from django.db.models import Sum
from .models import Siswa

@role_required("admin")
def admin_dashboard(request):

    # Ambil semua data siswa dari database
    siswa = Siswa.objects.all()

    # Jumlah siswa
    total_siswa = siswa.count()

    # Total seluruh saldo siswa
    total_saldo = siswa.aggregate(
        total=Sum("saldo")
    )["total"] or 0

    context = {
        "total_siswa": total_siswa,
        "total_saldo": total_saldo,
    }

    return render(
        request,
        "core/admin_dashboard.html",
        context
    )

@role_required("admin", "guru")
def data_siswa(request):

    siswa = Siswa.objects.all().order_by("nama")

    keyword = request.GET.get("q", "").strip()

    if keyword:
        siswa = siswa.filter(
            nama__icontains=keyword
        ) | siswa.filter(
            nis__icontains=keyword
        )

    kelas = Kelas.objects.all().order_by("nama_kelas")

    context = {
        "siswa": siswa,
        "kelas": kelas,
        "keyword": keyword,
    }

    return render(
        request,
        "core/data_siswa.html",
        context
    )

@role_required("admin")
def tambah_siswa(request):

    kelas = Kelas.objects.all().order_by("nama_kelas")

    if request.method == "POST":

        nis = request.POST.get("nis", "").strip()
        nama = request.POST.get("nama", "").strip()
        kelas_id = request.POST.get("kelas_id", "").strip()
        saldo = request.POST.get("saldo", "0").strip()

        user = User.objects.create(
            username=nis,
            password=nis,
            role="siswa",
            nama=nama
        )

        Siswa.objects.create(
            user_id=user.id,
            nis=nis,
            nama=nama,
            kelas_id=kelas_id,
            saldo=saldo
        )

        return redirect("data_siswa")

    return render(
        request,
        "core/tambah_siswa.html",
        {"kelas": kelas}
    )

@role_required("admin")
def edit_siswa(request, id):

    siswa = get_object_or_404(Siswa, id=id)

    kelas = Kelas.objects.all().order_by("nama_kelas")

    if request.method == "POST":

        siswa.nis = request.POST.get("nis", "").strip()
        siswa.nama = request.POST.get("nama", "").strip()
        siswa.kelas_id = request.POST.get("kelas_id", "").strip()
        siswa.saldo = request.POST.get("saldo", "0").strip()

        siswa.save()

        return redirect("data_siswa")

    return render(
        request,
        "core/edit_siswa.html",
        {
            "siswa": siswa,
            "kelas": kelas
        }
    )

@role_required("admin")
def hapus_siswa(request, id):

    siswa = get_object_or_404(Siswa, id=id)

    if request.method == "POST":

        user_id = siswa.user_id

        siswa.delete()

        User.objects.filter(
            id=user_id,
            role="siswa"
        ).delete()

        return redirect("data_siswa")

    return render(
        request,
        "core/hapus_siswa.html",
        {
            "siswa": siswa
        }
    )

@role_required("admin")
def detail_siswa(request, id):
    siswa = get_object_or_404(Siswa, id=id)

    transaksi_list = Transaksi.objects.filter(
        siswa_id=siswa.id
    ).order_by("-tanggal")

    return render(
        request,
        "core/detail_siswa.html",
        {
            "siswa": siswa,
            "transaksi_list": transaksi_list
        }
    )

@role_required("guru")
def guru_dashboard(request):
    siswa = Siswa.objects.all()

    total_siswa = siswa.count()
    total_saldo = siswa.aggregate(total=Sum("saldo"))["total"] or 0

    context = {
        "total_siswa": total_siswa,
        "total_saldo": total_saldo,
    }

    return render(request, "core/guru_dashboard.html", context)

@role_required("siswa")
def siswa_dashboard(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    siswa = get_object_or_404(Siswa, user_id=user_id)

    kelas = Kelas.objects.filter(id=siswa.kelas_id).first()

    context = {
        "nama_siswa": siswa.nama,
        "nis": siswa.nis,
        "saldo": siswa.saldo,
        "nama_kelas": kelas.nama_kelas if kelas else "-",
    }

    return render(request, "core/siswa_dashboard.html", context)

@role_required("admin", "guru")
def transaksi(request):
    siswa_list = Siswa.objects.all().order_by("nama")

    if request.method == "POST":
        siswa_id = request.POST.get("siswa_id")
        jenis = request.POST.get("jenis")
        nominal = request.POST.get("nominal")
        keterangan = request.POST.get("keterangan", "").strip()

        siswa = get_object_or_404(Siswa, id=siswa_id)

        nominal = float(nominal)
        saldo_sebelum = float(siswa.saldo)

        if jenis == "setor":
            saldo_sesudah = saldo_sebelum + nominal

        elif jenis == "tarik":
            if nominal > saldo_sebelum:
                messages.error(request, "Saldo siswa tidak mencukupi.")
                return redirect("transaksi")

            saldo_sesudah = saldo_sebelum - nominal

        else:
            messages.error(request, "Jenis transaksi tidak valid.")
            return redirect("transaksi")

        siswa.saldo = saldo_sesudah
        siswa.save()

        Transaksi.objects.create(
            siswa_id=siswa.id,
            guru_id=None,
            jenis=jenis,
            nominal=nominal,
            saldo_sebelum=saldo_sebelum,
            saldo_sesudah=saldo_sesudah,
            keterangan=keterangan
        )

        messages.success(request, "Transaksi berhasil disimpan.")

        return redirect("transaksi")

    return render(
        request,
        "core/transaksi.html",
        {"siswa_list": siswa_list}
    )

@role_required("admin", "guru")
def riwayat_transaksi(request):
    transaksi_list = []

    transaksi_data = Transaksi.objects.all().order_by("-tanggal")

    for item in transaksi_data:
        siswa = Siswa.objects.filter(id=item.siswa_id).first()

        transaksi_list.append({
            "nama_siswa": siswa.nama if siswa else "Siswa tidak ditemukan",
            "jenis": item.jenis,
            "nominal": item.nominal,
            "keterangan": item.keterangan,
            "tanggal": item.tanggal,
        })

    return render(
        request,
        "core/riwayat_transaksi.html",
        {"transaksi_list": transaksi_list}
    )

@role_required("admin", "guru")
def laporan(request):
    transaksi_list = Transaksi.objects.all().order_by("-tanggal")

    total_setor = Transaksi.objects.filter(
        jenis="setor"
    ).aggregate(total=Sum("nominal"))["total"] or 0

    total_tarik = Transaksi.objects.filter(
        jenis="tarik"
    ).aggregate(total=Sum("nominal"))["total"] or 0

    context = {
        "transaksi_list": transaksi_list,
        "total_setor": total_setor,
        "total_tarik": total_tarik,
    }

    return render(request, "core/laporan.html", context)

@role_required("siswa")
def riwayat_siswa(request):
    user_id = request.session.get("user_id")

    siswa = get_object_or_404(
        Siswa,
        user_id=user_id
    )

    transaksi_list = Transaksi.objects.filter(
        siswa_id=siswa.id
    ).order_by("-tanggal")

    return render(
        request,
        "core/riwayat_siswa.html",
        {
            "transaksi_list": transaksi_list,
            "siswa": siswa,
        }
    )

def logout_view(request):
    request.session.flush()
    return redirect("login")


@role_required("admin")
def data_pengumuman(request):
    pengumuman = Pengumuman.objects.all().order_by("-tanggal")

    return render(
        request,
        "core/data_pengumuman.html",
        {
            "pengumuman": pengumuman
        }
    )
  
@role_required("admin")
def tambah_pengumuman(request):
    if request.method == "POST":
        judul = request.POST.get("judul", "").strip()
        isi = request.POST.get("isi", "").strip()

        Pengumuman.objects.create(
            judul=judul,
            isi=isi
        )

        return redirect("data_pengumuman")

    return render(
        request,
        "core/tambah_pengumuman.html"
    )
  
@role_required("siswa")
def pengumuman_siswa(request):
    pengumuman = Pengumuman.objects.all().order_by("-tanggal")

    return render(
        request,
        "core/pengumuman_siswa.html",
        {
            "pengumuman": pengumuman
        }
    )

@role_required("siswa")
def saldo_siswa(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    siswa = get_object_or_404(Siswa, user_id=user_id)

    return render(
        request,
        "core/saldo_siswa.html",
        {
            "nama_siswa": siswa.nama,
            "saldo": siswa.saldo,
        }
    )