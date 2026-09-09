/* ==========================================================================
   PORTOFOLIO NAYLA AZZAHRA R - JAVASCRIPT TERPADU (script.js)
   Satu file script terhubung untuk semua halaman web:
   - index.html   : Sistem navigasi per-slide & kontrol keyboard
   - about.html   : Smooth scroll menu pintas & interaksi
   - contact.html : Validasi formulir & notifikasi pengiriman pesan
   ========================================================================== */

// --------------------------------------------------------------------------
// 1. SISTEM KONTROL SLIDE (KHUSUS INDEX.HTML)
// --------------------------------------------------------------------------
let currentSlide = 0;

function showSlide(index) {
    const slides = document.querySelectorAll('.slide-item');
    if (!slides || slides.length === 0) return;

    // Batasi index dalam rentang slide yang valid
    if (index < 0) index = 0;
    if (index >= slides.length) index = slides.length - 1;
    currentSlide = index;

    // 1. Tampilkan slide terpilih dan sembunyikan slide lainnya
    slides.forEach((slide, idx) => {
        if (idx === currentSlide) {
            slide.classList.add('active');
        } else {
            slide.classList.remove('active');
        }
    });

    // 2. Tandai item menu navigasi atas yang aktif
    const menuItems = document.querySelectorAll('#menu li');
    if (menuItems.length >= slides.length) {
        menuItems.forEach((item, idx) => {
            if (idx === currentSlide) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    // 3. Perbarui titik navigasi (dots)
    const dots = document.querySelectorAll('.slide-dot');
    dots.forEach((dot, idx) => {
        if (idx === currentSlide) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });

    // 4. Perbarui teks indikator (Slide X dari Y)
    const indicator = document.getElementById('slide-indicator-text');
    if (indicator) {
        indicator.textContent = 'Slide ' + (currentSlide + 1) + ' dari ' + slides.length;
    }

    // 5. Atur status tombol Sebelumnya & Selanjutnya
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    if (btnPrev) btnPrev.disabled = (currentSlide === 0);
    if (btnNext) btnNext.disabled = (currentSlide === slides.length - 1);

    // 6. Gulir halus ke bagian atas wrapper
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function changeSlide(step) {
    showSlide(currentSlide + step);
}

function initSlideSystem() {
    const slides = document.querySelectorAll('.slide-item');
    if (!slides || slides.length === 0) return;

    // Buat titik navigasi (dots) secara dinamis
    const dotsContainer = document.getElementById('slide-dots-container');
    if (dotsContainer) {
        dotsContainer.innerHTML = '';
        slides.forEach((_, i) => {
            const dot = document.createElement('button');
            dot.type = 'button';
            dot.className = 'slide-dot' + (i === 0 ? ' active' : '');
            dot.title = 'Buka Slide ' + (i + 1);
            dot.addEventListener('click', () => showSlide(i));
            dotsContainer.appendChild(dot);
        });
    }

    // Hubungkan tombol navigasi slide
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    if (btnPrev) {
        btnPrev.addEventListener('click', () => changeSlide(-1));
    }
    if (btnNext) {
        btnNext.addEventListener('click', () => changeSlide(1));
    }

    // Navigasi Keyboard: Tombol Panah Kiri (Sebelumnya) & Panah Kanan (Selanjutnya)
    window.addEventListener('keydown', (e) => {
        // Jangan aktifkan jika user sedang mengetik di input atau textarea
        if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

        if (e.key === 'ArrowRight' || e.key === 'PageDown') {
            changeSlide(1);
        } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
            changeSlide(-1);
        }
    });

    // Tampilkan slide pertama saat inisialisasi
    showSlide(0);
}

// --------------------------------------------------------------------------
// 2. VALIDASI & INTERAKSI FORMULIR KONTAK (KHUSUS CONTACT.HTML)
// --------------------------------------------------------------------------
function initContactForm() {
    const form = document.getElementById('form-kontak');
    if (!form) return;

    const statusBox = document.getElementById('form-status');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const nama = document.getElementById('nama')?.value.trim();
        const email = document.getElementById('email')?.value.trim();
        const subjek = document.getElementById('subjek')?.value.trim();
        const pesan = document.getElementById('pesan')?.value.trim();

        // Validasi kelengkapan
        if (!nama || !email || !subjek || !pesan) {
            if (statusBox) {
                statusBox.style.display = 'block';
                statusBox.className = 'status-box';
                statusBox.style.borderColor = '#dc2626';
                statusBox.style.backgroundColor = '#fef2f2';
                statusBox.style.color = '#991b1b';
                statusBox.innerHTML = '<strong>Peringatan:</strong> Mohon lengkapi seluruh kolom formulir sebelum mengirim.';
            } else {
                alert('Mohon lengkapi seluruh kolom formulir sebelum mengirim.');
            }
            return;
        }

        // Tampilkan konfirmasi keberhasilan
        if (statusBox) {
            statusBox.style.display = 'block';
            statusBox.className = 'status-box';
            statusBox.style.borderColor = '#16a34a';
            statusBox.style.backgroundColor = '#f0fdf4';
            statusBox.style.color = '#166534';
            statusBox.innerHTML = '<strong>Terima kasih, ' + nama + '!</strong> Pesan Anda mengenai <em>"' + subjek + '"</em> telah berhasil dikirimkan.';
            statusBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            alert('Terima kasih, ' + nama + '! Pesan Anda telah berhasil dikirimkan.');
        }

        // Reset formulir
        form.reset();
    });
}

// --------------------------------------------------------------------------
// 3. SMOOTH SCROLL MENU PINTAS (ABOUT.HTML & HALAMAN LAINNYA)
// --------------------------------------------------------------------------
function initSmoothNavigation() {
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId !== '#' && !this.hasAttribute('onclick')) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
}

// --------------------------------------------------------------------------
// 4. FITUR GLOBAL (MENU AKTIF & TAHUN FOOTER)
// --------------------------------------------------------------------------
function initGlobalFeatures() {
    const footerYearElements = document.querySelectorAll('.footer-year');
    const currentYear = new Date().getFullYear();
    footerYearElements.forEach(el => {
        el.textContent = currentYear;
    });

    const hasSlides = document.querySelector('.slide-item');
    if (!hasSlides) {
        const currentPath = window.location.pathname.split('/').pop() || 'index.html';
        const menuLinks = document.querySelectorAll('#menu li a');
        menuLinks.forEach(link => {
            const linkHref = link.getAttribute('href');
            if (linkHref && (linkHref === currentPath || (currentPath === '' && linkHref === 'index.html'))) {
                link.parentElement.classList.add('active');
            } else {
                link.parentElement.classList.remove('active');
            }
        });
    }
}

// --------------------------------------------------------------------------
// 5. INISIALISASI SAAT DOKUMEN SIAP
// --------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    initSlideSystem();
    initContactForm();
    initSmoothNavigation();
    initGlobalFeatures();
});
