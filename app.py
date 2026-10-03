from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CONTENT = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AHA! - Asisten Hadapi Analisis</title>
  
  <!-- Firebase SDK -->
  <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore-compat.js"></script>

  <!-- Google Fonts Inter -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, sans-serif; }
    body { background-color: #f8fafc; min-height: 100vh; color: #1e293b; overflow-x: hidden; }

    #loginSectionWrapper {
      background-color: #0f172a; 
      min-height: 100vh; 
      display: flex;
      align-items: center; 
      justify-content: center; 
      position: relative; 
      overflow: hidden; 
      padding: 20px;
    }

    .math-bg-container {
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      pointer-events: none;
      z-index: 0;
    }

    .math-symbol {
      position: absolute;
      color: rgba(255, 255, 255, 0.12);
      font-family: 'Cambria Math', 'Times New Roman', serif;
      font-weight: bold;
      user-select: none;
      animation: floatMove infinite ease-in-out alternate;
    }

    @keyframes floatMove {
      0% { transform: translateY(0px) rotate(0deg) scale(1); opacity: 0.08; }
      50% { opacity: 0.18; }
      100% { transform: translateY(-40px) rotate(12deg) scale(1.1); opacity: 0.1; }
    }

    .login-card { 
      background: #ffffff; 
      border-radius: 24px; 
      display: grid; 
      grid-template-columns: 1fr 1fr; 
      overflow: hidden; 
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); 
      width: 100%; 
      max-width: 960px; 
      z-index: 1;
      position: relative;
    }

    .card-left { padding: 44px 36px; background: #f8fafc; border-right: 1px solid #f1f5f9; display: flex; flex-direction: column; justify-content: center; }
    .bulb-icon-box { width: 52px; height: 52px; background-color: #fef3c7; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 26px; margin-bottom: 24px; }
    .brand-title { font-size: 24px; font-weight: 800; color: #0f172a; }
    .brand-title span { color: #2563eb; }
    .brand-desc { font-size: 13.5px; color: #64748b; margin-top: 10px; line-height: 1.55; margin-bottom: 28px; }
    .feature-pill { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 14px 18px; margin-bottom: 12px; display: flex; align-items: center; gap: 12px; font-size: 13px; font-weight: 600; color: #334155; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }
    
    .card-right { padding: 44px 38px; background-color: #ffffff; display: flex; flex-direction: column; justify-content: center; }
    .form-title { font-size: 22px; font-weight: 800; color: #0f172a; }
    .form-subtitle { font-size: 13.5px; color: #64748b; margin-top: 6px; margin-bottom: 26px; }
    .form-group { margin-bottom: 18px; }
    .form-label { display: block; font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 8px; }
    .form-label span { color: #ef4444; }
    .input-field { width: 100%; padding: 12px 16px; font-size: 13.5px; border: 1px solid #cbd5e1; border-radius: 12px; outline: none; transition: all 0.2s; background-color: #f8fafc; color: #0f172a; }
    .input-field::placeholder { color: #94a3b8; }
    .input-field:focus { border-color: #2563eb; background-color: #ffffff; box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
    
    .avatar-container { display: flex; gap: 10px; overflow-x: auto; padding: 6px 2px 12px 2px; scrollbar-width: thin; }
    .avatar-item { flex: 0 0 auto; width: 56px; height: 56px; border-radius: 50%; border: 2px solid #e2e8f0; cursor: pointer; overflow: hidden; background: #f1f5f9; transition: all 0.2s; }
    .avatar-item:hover { border-color: #94a3b8; transform: translateY(-2px); }
    .avatar-item.active { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.25); transform: scale(1.08); background: #eff6ff; }
    .avatar-item img { width: 100%; height: 100%; object-fit: cover; }
    
    .btn-login { width: 100%; background-color: #2563eb; color: #ffffff; font-size: 14px; font-weight: 700; padding: 13px; border: none; border-radius: 12px; cursor: pointer; margin-top: 8px; transition: all 0.2s; }
    .btn-login:hover { background-color: #1d4ed8; }

    #forumSection { display: none; }
    .top-navbar { background: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 12px 32px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }
    .nav-left { display: flex; align-items: center; gap: 12px; }
    .nav-logo-box { width: 40px; height: 40px; background: #2563eb; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px; }
    .nav-title { font-weight: 800; font-size: 18px; color: #0f172a; }
    .nav-subtitle { font-size: 11px; color: #64748b; font-weight: 500; }
    .nav-search { width: 380px; position: relative; }
    .nav-search input { width: 100%; background: #f1f5f9; border: 1px solid transparent; padding: 10px 16px 10px 40px; border-radius: 20px; font-size: 13px; outline: none; }
    .nav-search input:focus { background: #ffffff; border-color: #2563eb; }
    .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #94a3b8; font-size: 14px; }
    .nav-profile { display: flex; align-items: center; gap: 12px; }
    .nav-avatar { width: 42px; height: 42px; border-radius: 50%; background: #f1f5f9; border: 1px solid #e2e8f0; }
    .user-info-meta { text-align: right; }
    .user-name-line { font-size: 13px; font-weight: 700; color: #0f172a; }
    .user-badge { display: inline-flex; align-items: center; gap: 4px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 2px 8px; font-size: 11px; font-weight: 700; color: #1d4ed8; margin-top: 2px; }
    .btn-logout { background: #f1f5f9; color: #64748b; border: none; padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer; margin-left: 8px; }
    .btn-logout:hover { background: #fee2e2; color: #dc2626; }

    .forum-container { max-width: 1280px; margin: 24px auto; padding: 0 24px; display: grid; grid-template-columns: 240px 1fr 280px; gap: 24px; }
    .section-label { font-size: 11px; font-weight: 700; color: #94a3b8; letter-spacing: 0.05em; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }
    .nav-menu-item { display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; border-radius: 12px; font-size: 13px; font-weight: 600; color: #475569; cursor: pointer; margin-bottom: 4px; }
    .nav-menu-item.active { background: #eff6ff; color: #2563eb; }
    .badge-count { background: #f1f5f9; color: #64748b; font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: 700; }
    .sidebar-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 18px; margin-bottom: 20px; }
    .empty-sidebar-text { font-size: 12px; color: #94a3b8; line-height: 1.5; }
    .folder-item { display: flex; justify-content: space-between; align-items: center; font-size: 12.5px; font-weight: 600; color: #334155; padding: 6px 0; cursor: pointer; }
    .folder-item:hover { color: #2563eb; }

    .tag-container { display: flex; flex-wrap: wrap; gap: 8px; }
    .tag-pill { background: #f1f5f9; color: #475569; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer; }
    .tag-pill.active { background: #0f172a; color: #ffffff; }

    .feed-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
    .feed-title { font-size: 18px; font-weight: 700; color: #0f172a; }
    .feed-count { font-size: 13px; color: #94a3b8; font-weight: 500; }

    .empty-feed-card { background: #ffffff; border: 1px dashed #cbd5e1; border-radius: 20px; padding: 60px 20px; text-align: center; }
    .empty-feed-icon { font-size: 48px; margin-bottom: 16px; display: inline-block; }
    .empty-feed-title { font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 6px; }
    .empty-feed-sub { font-size: 13px; color: #64748b; max-width: 360px; margin: 0 auto 20px auto; line-height: 1.5; }

    .post-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; margin-bottom: 16px; position: relative; }
    .post-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
    .post-author { display: flex; align-items: center; gap: 10px; }
    .post-author img { width: 38px; height: 38px; border-radius: 50%; border: 1px solid #e2e8f0; }
    .post-author-name { font-size: 13.5px; font-weight: 700; color: #0f172a; }
    .post-author-dept { font-size: 11px; color: #64748b; }
    .category-badge { background: #f1f5f9; color: #2563eb; font-weight: 700; font-size: 11px; padding: 4px 10px; border-radius: 6px; }
    .post-body { font-size: 14px; color: #1e293b; line-height: 1.6; margin-bottom: 14px; white-space: pre-line; }
    
    .post-image-box { margin-bottom: 14px; border-radius: 12px; overflow: hidden; max-height: 380px; background: #0f172a; cursor: pointer; text-align: center; }
    .post-image-box img { max-width: 100%; max-height: 380px; object-fit: contain; }

    .post-actions { display: flex; align-items: center; gap: 16px; border-top: 1px solid #f1f5f9; padding-top: 12px; }
    .action-btn { display: flex; align-items: center; gap: 6px; font-size: 12.5px; font-weight: 600; color: #64748b; background: transparent; border: none; cursor: pointer; padding: 6px 10px; border-radius: 8px; }
    .action-btn:hover { background: #f1f5f9; color: #2563eb; }
    .action-btn.active { color: #2563eb; background: #eff6ff; }
    .action-btn.bookmarked { color: #d97706; background: #fef3c7; }

    .btn-delete { background: #fee2e2; color: #dc2626; border: none; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; cursor: pointer; transition: background 0.2s; }
    .btn-delete:hover { background: #fca5a5; }
    
    .btn-delete-reply { background: transparent; color: #94a3b8; border: none; font-size: 12px; cursor: pointer; padding: 2px 6px; border-radius: 4px; transition: all 0.2s; }
    .btn-delete-reply:hover { color: #dc2626; background: #fee2e2; }

    .replies-container { margin-top: 16px; background: #f8fafc; border-radius: 12px; padding: 14px; border: 1px solid #f1f5f9; }
    .reply-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 10px; position: relative; }
    .reply-card.best-answer { border: 2px solid #22c55e; background: #f0fdf4; }
    .best-answer-tag { background: #22c55e; color: white; font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-bottom: 6px; }

    /* STYLING DEDIKASI TOMBOL UPLOAD JAWABAN */
    .btn-reply-upload {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #ffffff;
      color: #334155;
      border: 1px solid #cbd5e1;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }
    .btn-reply-upload:hover {
      background: #f1f5f9;
      border-color: #94a3b8;
      color: #0f172a;
    }

    .btn-create-post { width: 100%; background: #2563eb; color: #ffffff; font-size: 14px; font-weight: 700; padding: 14px; border: none; border-radius: 14px; cursor: pointer; margin-bottom: 20px; box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25); }
    .leaderboard-list { list-style: none; }
    .leaderboard-item { display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; }
    .leaderboard-user { display: flex; align-items: center; gap: 8px; font-size: 12.5px; font-weight: 600; }
    .leaderboard-user img { width: 28px; height: 28px; border-radius: 50%; }
    .leaderboard-pts { font-size: 12px; font-weight: 700; color: #2563eb; }

    .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
    .stat-box { background: #f8fafc; border-radius: 10px; padding: 12px; }
    .stat-label { font-size: 11px; color: #64748b; font-weight: 600; }
    .stat-val { font-size: 18px; font-weight: 800; color: #2563eb; margin-top: 2px; }

    .modal-overlay { position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px); display:none; align-items:center; justify-content:center; z-index: 1000; }
    .modal-card { background: white; width: 100%; max-width: 520px; border-radius: 20px; padding: 24px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }
    .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
    .modal-title { font-size: 16px; font-weight: 800; color: #0f172a; }
    .btn-close-modal { background: none; border: none; font-size: 20px; cursor: pointer; color: #94a3b8; }
    .img-preview { width: 100%; max-height: 180px; object-fit: contain; margin-top: 8px; border-radius: 8px; display: none; }

    @media (max-width: 900px) { .login-card, .forum-container { grid-template-columns: 1fr; } .nav-search { display: none; } }
  </style>
</head>
<body>

  <!-- LAYAR LOGIN -->
  <div id="loginSectionWrapper">
    <div class="math-bg-container" id="mathBgContainer"></div>

    <div class="login-card">
      <div class="card-left">
        <div class="bulb-icon-box">💡</div>
        <h1 class="brand-title">AHA! <span>Asisten Hadapi Analisis</span></h1>
        <p class="brand-desc">Forum tanya jawab dan diskusi akademik mahasiswa. Dapatkan momen "aha!" paham materi lewat bantuan kawan sejawat.</p>
        <div class="feature-pill"><span>📌</span> Koleksi Folder Penyimpanan Pribadi</div>
        <div class="feature-pill"><span>⭐</span> Fitur Jawaban Terbaik & Poin Level</div>
        <div class="feature-pill"><span>🏆</span> Peringkat Penjawab Teraktif Harian</div>
      </div>

      <div class="card-right">
        <h2 class="form-title">Buat Profil Anda</h2>
        <p class="form-subtitle">Lengkapi data diri untuk masuk ke forum.</p>
        
        <form onsubmit="handleLogin(event)">
          <div class="form-group">
            <label class="form-label">Nama Lengkap / Panggilan <span>*</span></label>
            <input type="text" id="nama" class="input-field" placeholder="Contoh: Budi Pratama" required>
          </div>
          
          <div class="form-group">
            <label class="form-label">Jurusan & Angkatan <span>*</span></label>
            <input type="text" id="jurusan" class="input-field" placeholder="Contoh: Teknik Informatika '23" required>
          </div>
          
          <div class="form-group">
            <label class="form-label">Pilih Avatar Profile <span>*</span></label>
            <div class="avatar-container" id="avatarList"></div>
          </div>
          
          <button type="submit" class="btn-login">Masuk ke Forum AHA! &rsaquo;</button>
        </form>
      </div>
    </div>
  </div>

  <!-- LAYAR DASHBOARD FORUM -->
  <div id="forumSection">
    
    <div class="top-navbar">
      <div class="nav-left">
        <div class="nav-logo-box">💡</div>
        <div>
          <div class="nav-title">AHA!</div>
          <div class="nav-subtitle">Asisten Hadapi Analisis</div>
        </div>
      </div>

      <div class="nav-search">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" oninput="handleSearch()" placeholder="Cari pertanyaan, rumus, atau mata kuliah...">
      </div>

      <div class="nav-profile">
        <img id="userAvatar" class="nav-avatar" src="">
        <div class="user-info-meta">
          <div class="user-name-line"><span id="userName">-</span> • <span id="userDept" style="color:#64748b; font-weight:normal;">-</span></div>
          <div class="user-badge" id="userBadge">🌱 Pemula (0 pts)</div>
        </div>
        <button class="btn-logout" onclick="handleLogout()" title="Keluar">Keluar 🚪</button>
      </div>
    </div>

    <div class="forum-container">
      
      <div>
        <div class="sidebar-card">
          <div class="section-label">NAVIGASI UTAMA</div>
          <div class="nav-menu-item active" id="navAll" onclick="switchNavFilter('all')">🌐 Jelajah Forum</div>
          <div class="nav-menu-item" id="navMyQuestions" onclick="switchNavFilter('myQuestions')">❓ Pertanyaan Saya <span class="badge-count" id="countMyQuestions">0</span></div>
          <div class="nav-menu-item" id="navMyAnswers" onclick="switchNavFilter('myAnswers')">💬 Jawaban Saya <span class="badge-count" id="countMyAnswers">0</span></div>
          <div class="nav-menu-item" id="navMySaved" onclick="switchNavFilter('mySaved')">🔖 Koleksi Saya <span class="badge-count" id="countMySaved">0</span></div>
        </div>

        <div class="sidebar-card">
          <div class="section-label">FOLDER KOLEKSI <span style="color:#2563eb; cursor:pointer;" onclick="openCreateFolderModal()">+ FOLDER</span></div>
          <div id="folderListContainer">
            <p class="empty-sidebar-text">Belum ada folder. Klik <b>+ FOLDER</b> untuk membuat.</p>
          </div>
        </div>

        <div class="sidebar-card">
          <div class="section-label">KATEGORI TOPIK</div>
          <div class="tag-container" id="categoryTagsContainer">
            <div class="tag-pill active" onclick="filterCategory('Semua', this)">Semua</div>
            <div class="tag-pill" onclick="filterCategory('Kalkulus', this)">#Kalkulus</div>
            <div class="tag-pill" onclick="filterCategory('Pemrograman', this)">#Pemrograman</div>
            <div class="tag-pill" onclick="filterCategory('Statistika', this)">#Statistika</div>
          </div>
        </div>
      </div>

      <div>
        <div class="feed-header">
          <div class="feed-title" id="feedTitleText">Diskusi Terbaru</div>
          <div class="feed-count" id="totalQuestionsCount">0 Pertanyaan</div>
        </div>

        <div id="postsFeedContainer"></div>
      </div>

      <div>
        <button class="btn-create-post" onclick="openNewQuestionModal()">+ Buat Pertanyaan Baru</button>

        <div class="sidebar-card">
          <div class="section-label">🏆 PERINGKAT HARIAN HARI INI</div>
          <ul class="leaderboard-list" id="leaderboardContainer">
            <p class="empty-sidebar-text">Belum ada peringkat harian. Mulai menjawab pertanyaan!</p>
          </ul>
        </div>

        <div class="sidebar-card">
          <div class="section-label">STATISTIK KOMUNITAS</div>
          <div class="stat-grid">
            <div class="stat-box">
              <div class="stat-label">Pertanyaan</div>
              <div class="stat-val" id="statQuestions">0</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">Solusi</div>
              <div class="stat-val" id="statSolutions">0</div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- MODAL PERTANYAAN -->
  <div class="modal-overlay" id="questionModal">
    <div class="modal-card">
      <div class="modal-header">
        <div class="modal-title">📝 Buat Pertanyaan Baru</div>
        <button class="btn-close-modal" onclick="closeModal('questionModal')">&times;</button>
      </div>
      <form id="questionForm" onsubmit="submitNewQuestion(event)">
        <div class="form-group">
          <label class="form-label">Kategori Topik <span>*</span></label>
          <input type="text" id="qCategory" class="input-field" placeholder="Misal: Kalkulus, Pemrograman, Biologi..." required>
        </div>
        <div class="form-group">
          <label class="form-label">Detail Pertanyaan <span>*</span></label>
          <textarea id="qBody" class="input-field" style="height:120px; resize:none;" placeholder="Tuliskan pertanyaan atau bagian soal yang membuat Anda bingung..." required></textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Upload Foto / Gambar Soal (Opsional)</label>
          <input type="file" id="qImageInput" accept="image/*" class="input-field" onchange="previewImage(event)">
          <img id="imagePreview" class="img-preview" src="">
        </div>
        <button type="submit" id="btnSubmitQuestion" class="btn-login" style="margin-top:12px;">Kirim Pertanyaan</button>
      </form>
    </div>
  </div>

  <!-- MODAL BOOKMARK -->
  <div class="modal-overlay" id="bookmarkModal">
    <div class="modal-card" style="max-width:380px;">
      <div class="modal-header">
        <div class="modal-title">🔖 Simpan ke Folder Koleksi</div>
        <button class="btn-close-modal" onclick="closeModal('bookmarkModal')">&times;</button>
      </div>
      <p style="font-size:12.5px; color:#64748b; margin-bottom:12px;">Pilih folder koleksi untuk menyimpan pertanyaan ini:</p>
      <div id="bookmarkFolderPicker"></div>
    </div>
  </div>

  <script>
    // Utility Sanitasi HTML
    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }

    // UTILITY KOMPRESI GAMBAR (Mengubah foto besar HP menjadi Base64 efisien)
    function compressImage(file, maxDimension, quality, callback) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
          const canvas = document.createElement('canvas');
          let width = img.width;
          let height = img.height;

          if (width > height) {
            if (width > maxDimension) {
              height = Math.round((height * maxDimension) / width);
              width = maxDimension;
            }
          } else {
            if (height > maxDimension) {
              width = Math.round((width * maxDimension) / height);
              height = maxDimension;
            }
          }

          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, width, height);

          const base64Url = canvas.toDataURL('image/jpeg', quality);
          callback(base64Url);
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    // FIREBASE SETUP
    const firebaseConfig = {
      apiKey: "YOUR_API_KEY",
      authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
      projectId: "YOUR_PROJECT_ID",
      storageBucket: "YOUR_PROJECT_ID.appspot.com",
      messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
      appId: "YOUR_APP_ID"
    };

    let db = null;
    try {
      firebase.initializeApp(firebaseConfig);
      db = firebase.firestore();
    } catch(e) {
      console.warn("Firebase tidak terkonfigurasi, menggunakan mode LocalStorage.", e);
    }

    // ANIMASI SIMBOL MATEMATIKA
    const mathSymbols = ['∫', 'π', '∑', '√x', 'f(x)', '∞', 'Δ', 'θ', 'lim', 'dy/dx', 'A∩B', 'X²', '∇', 'α', 'β', 'λ'];
    const bgContainer = document.getElementById('mathBgContainer');
    if (bgContainer) {
      for (let i = 0; i < 26; i++) {
        const sym = document.createElement('div');
        sym.className = 'math-symbol';
        sym.textContent = mathSymbols[Math.floor(Math.random() * mathSymbols.length)];
        sym.style.left = Math.random() * 95 + '%';
        sym.style.top = Math.random() * 95 + '%';
        sym.style.fontSize = (Math.floor(Math.random() * 30) + 24) + 'px';
        sym.style.animationDuration = (Math.random() * 6 + 4) + 's';
        sym.style.animationDelay = Math.random() * 5 + 's';
        bgContainer.appendChild(sym);
      }
    }

    // STATE APLIKASI
    let currentUser = null;
    let localQuestions = []; 
    let localUsers = [];
    let localFolders = JSON.parse(localStorage.getItem('aha_folders') || '[]');
    let localBookmarks = JSON.parse(localStorage.getItem('aha_bookmarks') || '{}'); 
    
    let activeNavFilter = 'all';
    let selectedCategory = 'Semua';
    let activeSearchTerm = '';
    let targetBookmarkQId = null;
    let tempImageBase64 = '';
    let tempReplyImages = {};

    const formalAvatarConfigs = [
      { label: 'Wanita Hijab 1', url: 'https://api.dicebear.com/7.x/avataaars/svg?top=hijab&hatColor=262e33&clothing=blazerAndShirt&clothesColor=262e33&skinColor=edb98a&eyes=default&mouth=smile&accessoriesProbability=0' },
      { label: 'Wanita Hijab 2', url: 'https://api.dicebear.com/7.x/avataaars/svg?top=hijab&hatColor=3c4f5c&clothing=collarAndSweater&clothesColor=2563eb&skinColor=fd9841&eyes=default&mouth=smile&accessoriesProbability=0' },
      { label: 'Wanita Rambut Panjang', url: 'https://api.dicebear.com/7.x/avataaars/svg?top=straight01&hairColor=2c1b18&clothing=blazerAndShirt&clothesColor=3c4f5c&skinColor=edb98a&eyes=default&mouth=smile&accessoriesProbability=0' },
      { label: 'Wanita Rambut Diikat', url: 'https://api.dicebear.com/7.x/avataaars/svg?top=bun&hairColor=2c1b18&clothing=collarAndSweater&clothesColor=2563eb&skinColor=fd9841&eyes=default&mouth=smile&accessoriesProbability=0' },
      { label: 'Pria 1', url: 'https://api.dicebear.com/7.x/avataaars/svg?top=shortFlat&hairColor=2c1b18&clothing=blazerAndShirt&clothesColor=262e33&skinColor=edb98a&eyes=default&mouth=smile&facialHairProbability=0&accessoriesProbability=0' },
      { label: 'Pria 2', url: 'https://api.dicebear.com/7.x/avataaars/svg?top=shortWaved&hairColor=2c1b18&clothing=collarAndSweater&clothesColor=3c4f5c&skinColor=fd9841&eyes=default&mouth=smile&facialHairProbability=0&accessoriesProbability=0' },
      { label: 'Pria 3', url: 'https://api.dicebear.com/7.x/avataaars/svg?top=theCaesar&hairColor=2c1b18&clothing=blazerAndShirt&clothesColor=2563eb&skinColor=d08b5b&eyes=default&mouth=smile&facialHairProbability=0&accessoriesProbability=0' },
      { label: 'Pria 4', url: 'https://api.dicebear.com/7.x/avataaars/svg?top=shortCurly&hairColor=2c1b18&clothing=collarAndSweater&clothesColor=515a6b&skinColor=edb98a&eyes=default&mouth=smile&facialHairProbability=0&accessoriesProbability=0' }
    ];

    const avatarContainer = document.getElementById('avatarList');
    if (avatarContainer) {
      formalAvatarConfigs.forEach((cfg, index) => {
        const div = document.createElement('div');
        div.className = `avatar-item ${index === 0 ? 'active' : ''}`;
        div.title = cfg.label;
        div.innerHTML = `<img src="${cfg.url}" alt="${cfg.label}">`;
        div.onclick = () => {
          document.querySelectorAll('.avatar-item').forEach(el => el.classList.remove('active'));
          div.classList.add('active');
        };
        avatarContainer.appendChild(div);
      });
    }

    window.onload = () => {
      const savedUser = localStorage.getItem('aha_user');
      if (savedUser) {
        try {
          currentUser = JSON.parse(savedUser);
          initDashboard();
        } catch(e) {
          localStorage.removeItem('aha_user');
        }
      }
    };

    function handleLogin(e) {
      e.preventDefault();
      const nama = document.getElementById('nama').value.trim();
      const jurusan = document.getElementById('jurusan').value.trim();
      const activeAvatarEl = document.querySelector('.avatar-item.active img');
      const avatarSrc = activeAvatarEl ? activeAvatarEl.src : formalAvatarConfigs[0].url;
      const cleanNameId = nama.toLowerCase().trim().replace(/[^a-z0-9]/g, '_');
      const userId = 'user_' + (cleanNameId || Date.now());

      currentUser = { id: userId, nama, jurusan, avatarSrc, points: 0 };
      localStorage.setItem('aha_user', JSON.stringify(currentUser));
      
      if (db && firebaseConfig.apiKey !== "YOUR_API_KEY") {
        db.collection("users").doc(userId).set(currentUser, { merge: true }).catch(err => console.warn(err));
      }

      initDashboard();
    }

    function handleLogout() {
      localStorage.removeItem('aha_user');
      currentUser = null;
      location.reload();
    }

    function initDashboard() {
      document.getElementById('userName').textContent = currentUser.nama;
      document.getElementById('userDept').textContent = currentUser.jurusan;
      document.getElementById('userAvatar').src = currentUser.avatarSrc;

      document.getElementById('loginSectionWrapper').style.display = 'none';
      document.getElementById('forumSection').style.display = 'block';

      renderFolders();
      loadData();
    }

    function loadData() {
      const savedQ = localStorage.getItem('aha_questions');
      if (savedQ) { try { localQuestions = JSON.parse(savedQ); } catch(e){} }
      const savedU = localStorage.getItem('aha_users');
      if (savedU) { try { localUsers = JSON.parse(savedU); } catch(e){} }

      renderFeedAndStats();
      renderLeaderboard();

      if (db && firebaseConfig.apiKey !== "YOUR_API_KEY") {
        try {
          db.collection("questions").orderBy("createdAt", "desc").onSnapshot(snapshot => {
            if (snapshot && snapshot.docs) {
              localQuestions = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
              saveLocalQuestions();
              renderFeedAndStats();
            }
          });

          db.collection("users").onSnapshot(snapshot => {
            if (snapshot && snapshot.docs) {
              localUsers = snapshot.docs.map(doc => doc.data());
              localStorage.setItem('aha_users', JSON.stringify(localUsers));
              const myData = localUsers.find(u => u.id === currentUser.id);
              if(myData) {
                currentUser.points = myData.points || 0;
                updateUserBadgeDisplay();
              }
              renderLeaderboard();
            }
          });
        } catch(err) {
          console.warn("Firestore error fallback to local storage:", err);
        }
      }
    }

    function saveLocalQuestions() {
      try {
        localStorage.setItem('aha_questions', JSON.stringify(localQuestions));
      } catch(e) {
        console.warn("Penyimpanan lokal penuh, membersihkan cache lama.", e);
      }
    }

    function getUserBadge(points) {
      if (points >= 100) return { label: '👑 Master', pts: points };
      if (points >= 50) return { label: '⭐ Ahli', pts: points };
      if (points >= 20) return { label: '📚 Pembelajar', pts: points };
      return { label: '🌱 Pemula', pts: points };
    }

    function updateUserBadgeDisplay() {
      const badge = getUserBadge(currentUser.points || 0);
      document.getElementById('userBadge').textContent = `${badge.label} (${badge.pts} pts)`;
    }

    function openNewQuestionModal() { document.getElementById('questionModal').style.display = 'flex'; }
    function closeModal(id) { 
      document.getElementById(id).style.display = 'none'; 
      if(id === 'questionModal') {
        document.getElementById('imagePreview').style.display = 'none';
        tempImageBase64 = '';
      }
    }

    // PREVIEW GAMBAR PERTANYAAN DENGAN KOMPRESI
    function previewImage(event) {
      const file = event.target.files && event.target.files[0];
      if (file) {
        compressImage(file, 800, 0.7, (compressedBase64) => {
          tempImageBase64 = compressedBase64;
          const imgPreview = document.getElementById('imagePreview');
          imgPreview.src = tempImageBase64;
          imgPreview.style.display = 'block';
        });
      }
    }

    // PREVIEW GAMBAR JAWABAN/BALASAN DENGAN KOMPRESI
    function previewReplyImage(event, qId) {
      const file = event.target.files && event.target.files[0];
      if (file) {
        compressImage(file, 800, 0.7, (compressedBase64) => {
          tempReplyImages[qId] = compressedBase64;
          const previewContainer = document.getElementById(`replyImgPreviewContainer_${qId}`);
          const previewEl = document.getElementById(`replyImgPreview_${qId}`);
          if (previewEl) previewEl.src = tempReplyImages[qId];
          if (previewContainer) previewContainer.style.display = 'block';
        });
      }
    }

    function clearReplyImage(qId) {
      delete tempReplyImages[qId];
      const previewContainer = document.getElementById(`replyImgPreviewContainer_${qId}`);
      const fileInput = document.getElementById(`replyFile_${qId}`);
      if (previewContainer) previewContainer.style.display = 'none';
      if (fileInput) fileInput.value = '';
    }

    function submitNewQuestion(e) {
      e.preventDefault();
      
      let rawCat = document.getElementById('qCategory').value.trim().replace(/^#/, '');
      if (!rawCat) return false;
      let category = rawCat.charAt(0).toUpperCase() + rawCat.slice(1);
      const body = document.getElementById('qBody').value.trim();

      if (!body) return false;

      const newQ = {
        id: 'q_' + Date.now(),
        authorId: currentUser.id,
        authorName: currentUser.nama,
        authorDept: currentUser.jurusan,
        authorAvatar: currentUser.avatarSrc,
        category,
        body,
        imageUrl: tempImageBase64 || '',
        upvotes: [],
        replies: [],
        createdAt: Date.now()
      };

      localQuestions.unshift(newQ);
      saveLocalQuestions();

      if (db && firebaseConfig.apiKey !== "YOUR_API_KEY") {
        db.collection("questions").doc(newQ.id).set(newQ).catch(err => console.warn(err));
      }

      closeModal('questionModal');
      document.getElementById('qCategory').value = '';
      document.getElementById('qBody').value = '';
      document.getElementById('qImageInput').value = '';
      document.getElementById('imagePreview').style.display = 'none';
      tempImageBase64 = '';

      renderFeedAndStats();
      return false;
    }

    function deleteQuestion(qId) {
      if (confirm("Apakah Anda yakin ingin menghapus pertanyaan ini? Seluruh balasan juga akan terhapus.")) {
        localQuestions = localQuestions.filter(q => q.id !== qId);
        saveLocalQuestions();

        if (db && firebaseConfig.apiKey !== "YOUR_API_KEY") {
          db.collection("questions").doc(qId).delete().catch(err => console.warn(err));
        }

        renderFeedAndStats();
      }
    }

    function deleteReply(qId, replyId) {
      if (confirm("Apakah Anda yakin ingin menghapus balasan ini?")) {
        const q = localQuestions.find(item => item.id === qId);
        if (!q) return;

        q.replies = (q.replies || []).filter(r => r.id !== replyId);
        saveLocalQuestions();

        if (db && firebaseConfig.apiKey !== "YOUR_API_KEY") {
          db.collection("questions").doc(qId).update({ replies: q.replies }).catch(err => console.warn(err));
        }

        renderFeedAndStats();
      }
    }

    function toggleUpvote(qId) {
      const q = localQuestions.find(item => item.id === qId);
      if(!q) return;

      if (!q.upvotes) q.upvotes = [];
      const hasUpvoted = q.upvotes.includes(currentUser.id);

      if (hasUpvoted) {
        q.upvotes = q.upvotes.filter(id => id !== currentUser.id);
        addPointsToUser(q.authorId, -2);
      } else {
        q.upvotes.push(currentUser.id);
        addPointsToUser(q.authorId, 2);
      }

      saveLocalQuestions();

      if (db && firebaseConfig.apiKey !== "YOUR_API_KEY") {
        db.collection("questions").doc(qId).update({ upvotes: q.upvotes }).catch(err => console.warn(err));
      }

      renderFeedAndStats();
    }

    function submitReply(qId, btnElement) {
      const input = document.getElementById(`replyInput_${qId}`);
      if (!input) return;
      const text = input.value.trim();
      const replyImg = tempReplyImages[qId] || '';

      if (!text && !replyImg) {
        alert("Harap tuliskan teks penjelasan atau lampirkan foto jawaban terlebih dahulu.");
        return;
      }

      const q = localQuestions.find(item => item.id === qId);
      if (!q) return;

      const reply = {
        id: 'r_' + Date.now(),
        authorId: currentUser.id,
        authorName: currentUser.nama,
        authorDept: currentUser.jurusan,
        authorAvatar: currentUser.avatarSrc,
        text: text,
        imageUrl: replyImg,
        isBest: false
      };

      if (!q.replies) q.replies = [];
      q.replies.push(reply);

      addPointsToUser(currentUser.id, 10);
      saveLocalQuestions();

      if (db && firebaseConfig.apiKey !== "YOUR_API_KEY") {
        db.collection("questions").doc(qId).update({ replies: q.replies }).catch(err => console.warn(err));
      }

      input.value = '';
      clearReplyImage(qId);
      renderFeedAndStats();
    }

    function markBestAnswer(qId, replyId) {
      const q = localQuestions.find(item => item.id === qId);
      if(!q || q.authorId !== currentUser.id) return;

      let bestAuthorId = null;
      q.replies = (q.replies || []).map(r => {
        if(r.id === replyId && !r.isBest) {
          bestAuthorId = r.authorId;
          return { ...r, isBest: true };
        }
        return r;
      });

      if (bestAuthorId) {
        addPointsToUser(bestAuthorId, 15);
      }

      saveLocalQuestions();

      if (db && firebaseConfig.apiKey !== "YOUR_API_KEY") {
        db.collection("questions").doc(qId).update({ replies: q.replies }).catch(err => console.warn(err));
      }

      renderFeedAndStats();
    }

    function addPointsToUser(userId, delta) {
      let u = localUsers.find(user => user.id === userId);
      if (u) {
        u.points = Math.max(0, (u.points || 0) + delta);
      } else if (currentUser && currentUser.id === userId) {
        currentUser.points = Math.max(0, (currentUser.points || 0) + delta);
        localUsers.push(currentUser);
      }

      if (currentUser && currentUser.id === userId) {
        currentUser.points = Math.max(0, (currentUser.points || 0) + delta);
        localStorage.setItem('aha_user', JSON.stringify(currentUser));
        updateUserBadgeDisplay();
      }

      localStorage.setItem('aha_users', JSON.stringify(localUsers));

      if (db && firebaseConfig.apiKey !== "YOUR_API_KEY") {
        const userRef = db.collection("users").doc(userId);
        userRef.get().then(doc => {
          if(doc.exists) {
            const currentPts = doc.data().points || 0;
            userRef.update({ points: Math.max(0, currentPts + delta) });
          }
        }).catch(err => console.warn(err));
      }
      renderLeaderboard();
    }

    function openCreateFolderModal() {
      const name = prompt("Masukkan nama Folder Koleksi baru:");
      if(name && name.trim() !== '') {
        const folderName = name.trim();
        if(!localFolders.includes(folderName)) {
          localFolders.push(folderName);
          localStorage.setItem('aha_folders', JSON.stringify(localFolders));
          renderFolders();
        }
      }
    }

    function renderFolders() {
      const container = document.getElementById('folderListContainer');
      if(localFolders.length === 0) {
        container.innerHTML = `<p class="empty-sidebar-text">Belum ada folder. Klik <b>+ FOLDER</b> untuk membuat.</p>`;
        return;
      }
      container.innerHTML = localFolders.map((f, idx) => `
        <div class="folder-item" onclick="filterByFolderIndex(${idx})">
          <span>📁 ${escapeHtml(f)}</span>
          <span style="font-size:11px; color:#94a3b8;">›</span>
        </div>
      `).join('');
    }

    function openBookmarkPicker(qId) {
      if(localFolders.length === 0) {
        alert("Buat folder koleksi terlebih dahulu melalui tombol '+ FOLDER' di sidebar sebelah kiri.");
        return;
      }
      targetBookmarkQId = qId;
      const picker = document.getElementById('bookmarkFolderPicker');
      picker.innerHTML = localFolders.map((f, idx) => `
        <button class="btn-login" style="background:#f1f5f9; color:#0f172a; margin-bottom:8px; text-align:left; font-weight:600;" onclick="saveToFolderByIndex(${idx})">
          📁 ${escapeHtml(f)}
        </button>
      `).join('');
      document.getElementById('bookmarkModal').style.display = 'flex';
    }

    function saveToFolderByIndex(idx) {
      const folderName = localFolders[idx];
      if (folderName && targetBookmarkQId) {
        localBookmarks[targetBookmarkQId] = folderName;
        localStorage.setItem('aha_bookmarks', JSON.stringify(localBookmarks));
        closeModal('bookmarkModal');
        renderFeedAndStats();
      }
    }

    function switchNavFilter(type) {
      activeNavFilter = type;
      document.querySelectorAll('.nav-menu-item').forEach(el => el.classList.remove('active'));
      
      if(type === 'all') document.getElementById('navAll').classList.add('active');
      if(type === 'myQuestions') document.getElementById('navMyQuestions').classList.add('active');
      if(type === 'myAnswers') document.getElementById('navMyAnswers').classList.add('active');
      if(type === 'mySaved') document.getElementById('navMySaved').classList.add('active');

      renderFeedAndStats();
    }

    function filterCategory(cat, el) {
      selectedCategory = cat;
      document.querySelectorAll('.tag-pill').forEach(tag => tag.classList.remove('active'));
      if(el) el.classList.add('active');
      renderFeedAndStats();
    }

    function filterByFolderIndex(idx) {
      const folderName = localFolders[idx];
      if (folderName) {
        activeNavFilter = 'folder_' + folderName;
        document.querySelectorAll('.nav-menu-item').forEach(el => el.classList.remove('active'));
        renderFeedAndStats();
      }
    }

    function handleSearch() {
      activeSearchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
      renderFeedAndStats();
    }

    function updateDynamicCategories() {
      const defaultCats = ['Semua', 'Kalkulus', 'Pemrograman', 'Statistika'];
      localQuestions.forEach(q => {
        if(q.category && !defaultCats.includes(q.category)) defaultCats.push(q.category);
      });

      const container = document.getElementById('categoryTagsContainer');
      container.innerHTML = defaultCats.map(cat => `
        <div class="tag-pill ${selectedCategory === cat ? 'active' : ''}" onclick="filterCategory('${escapeHtml(cat)}', this)">
          ${cat === 'Semua' ? 'Semua' : '#' + escapeHtml(cat)}
        </div>
      `).join('');
    }

    function renderFeedAndStats() {
      updateDynamicCategories();

      const myQCount = localQuestions.filter(q => q.authorId === currentUser.id).length;
      const myACount = localQuestions.filter(q => q.replies && q.replies.some(r => r.authorId === currentUser.id)).length;
      const mySCount = Object.keys(localBookmarks).length;

      document.getElementById('countMyQuestions').textContent = myQCount;
      document.getElementById('countMyAnswers').textContent = myACount;
      document.getElementById('countMySaved').textContent = mySCount;

      let filtered = [...localQuestions];

      if(activeNavFilter === 'myQuestions') {
        filtered = filtered.filter(q => q.authorId === currentUser.id);
        document.getElementById('feedTitleText').textContent = "Pertanyaan Saya";
      } else if(activeNavFilter === 'myAnswers') {
        filtered = filtered.filter(q => q.replies && q.replies.some(r => r.authorId === currentUser.id));
        document.getElementById('feedTitleText').textContent = "Jawaban Saya";
      } else if(activeNavFilter === 'mySaved') {
        filtered = filtered.filter(q => localBookmarks[q.id]);
        document.getElementById('feedTitleText').textContent = "Koleksi Tersimpan";
      } else if(activeNavFilter.startsWith('folder_')) {
        const targetFolder = activeNavFilter.replace('folder_', '');
        filtered = filtered.filter(q => localBookmarks[q.id] === targetFolder);
        document.getElementById('feedTitleText').textContent = `Folder: ${targetFolder}`;
      } else {
        document.getElementById('feedTitleText').textContent = "Diskusi Terbaru";
      }

      if(selectedCategory !== 'Semua') filtered = filtered.filter(q => q.category === selectedCategory);
      if(activeSearchTerm) {
        filtered = filtered.filter(q => 
          (q.body && q.body.toLowerCase().includes(activeSearchTerm)) ||
          (q.category && q.category.toLowerCase().includes(activeSearchTerm))
        );
      }

      document.getElementById('statQuestions').textContent = localQuestions.length;
      let totalSolutions = 0;
      localQuestions.forEach(q => totalSolutions += (q.replies ? q.replies.length : 0));
      document.getElementById('statSolutions').textContent = totalSolutions;
      document.getElementById('totalQuestionsCount').textContent = `${filtered.length} Pertanyaan`;

      const feedContainer = document.getElementById('postsFeedContainer');
      if (filtered.length === 0) {
        feedContainer.innerHTML = `
          <div class="empty-feed-card">
            <span class="empty-feed-icon">💬</span>
            <div class="empty-feed-title">Belum Ada Diskusi / Pertanyaan</div>
            <p class="empty-feed-sub">Jadilah yang pertama mengajukan pertanyaan atau diskusi di forum ini!</p>
            <button class="btn-create-post" style="width:auto; display:inline-block;" onclick="openNewQuestionModal()">+ Ajukan Pertanyaan Pertama</button>
          </div>
        `;
        return;
      }

      feedContainer.innerHTML = filtered.map(q => {
        const upvotesList = q.upvotes || [];
        const repliesList = q.replies || [];
        const isUpvoted = upvotesList.includes(currentUser.id);
        const folderSaved = localBookmarks[q.id];
        const isMyQuestion = (q.authorId === currentUser.id);

        return `
          <div class="post-card">
            <div class="post-header">
              <div class="post-author">
                <img src="${q.authorAvatar || ''}">
                <div>
                  <div class="post-author-name">${escapeHtml(q.authorName)}</div>
                  <div class="post-author-dept">${escapeHtml(q.authorDept)}</div>
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:8px;">
                <span class="category-badge">#${escapeHtml(q.category)}</span>
                ${isMyQuestion ? `<button class="btn-delete" onclick="deleteQuestion('${q.id}')" title="Hapus Pertanyaan">🗑️ Hapus</button>` : ''}
              </div>
            </div>

            <div class="post-body">${escapeHtml(q.body)}</div>

            ${q.imageUrl ? `<div class="post-image-box"><img src="${q.imageUrl}"></div>` : ''}

            <div class="post-actions">
              <button class="action-btn ${isUpvoted ? 'active' : ''}" onclick="toggleUpvote('${q.id}')">
                👍 <span>${upvotesList.length} Upvote</span>
              </button>
              <button class="action-btn">
                💬 <span>${repliesList.length} Balasan</span>
              </button>
              <button class="action-btn ${folderSaved ? 'bookmarked' : ''}" onclick="openBookmarkPicker('${q.id}')">
                🔖 <span>${folderSaved ? `Tersimpan (${escapeHtml(folderSaved)})` : 'Simpan'}</span>
              </button>
            </div>

            <div class="replies-container">
              ${repliesList.map(r => {
                const isMyReply = (r.authorId === currentUser.id);
                return `
                  <div class="reply-card ${r.isBest ? 'best-answer' : ''}">
                    ${r.isBest ? `<div class="best-answer-tag">⭐ JAWABAN TERBAIK</div>` : ''}
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                      <div style="font-weight:700; font-size:12px;">${escapeHtml(r.authorName)} <span style="font-weight:normal; color:#64748b;">(${escapeHtml(r.authorDept)})</span></div>
                      <div style="display:flex; align-items:center; gap:6px;">
                        ${(q.authorId === currentUser.id && !r.isBest) ? `
                          <button style="font-size:10px; background:#22c55e; color:white; border:none; padding:3px 6px; border-radius:4px; cursor:pointer;" onclick="markBestAnswer('${q.id}', '${r.id}')">
                            ⭐ Tandai Terbaik
                          </button>
                        ` : ''}
                        ${(isMyReply || isMyQuestion) ? `
                          <button class="btn-delete-reply" onclick="deleteReply('${q.id}', '${r.id}')" title="Hapus Balasan">🗑️</button>
                        ` : ''}
                      </div>
                    </div>
                    ${r.text ? `<div style="font-size:12.5px; color:#334155; white-space:pre-line;">${escapeHtml(r.text)}</div>` : ''}
                    ${r.imageUrl ? `<div style="margin-top:8px; max-height:240px; overflow:hidden; border-radius:8px; background:#0f172a; text-align:center;"><img src="${r.imageUrl}" style="max-width:100%; max-height:240px; object-fit:contain; border-radius:8px;"></div>` : ''}
                  </div>
                `;
              }).join('')}

              <!-- FORM BALASAN / JAWABAN KUSTOM DENGAN TOMBOL UPLOAD DEDIKASI -->
              <div class="reply-form-wrapper" style="margin-top: 14px; background: #ffffff; padding: 14px; border-radius: 12px; border: 1px solid #e2e8f0;">
                <div style="font-size: 12.5px; font-weight: 700; color: #0f172a; margin-bottom: 8px;">Tulis Jawaban / Penjelasan Anda:</div>
                
                <textarea id="replyInput_${q.id}" class="input-field" style="height: 75px; resize: none; margin-bottom: 10px; font-size: 13px;" placeholder="Tuliskan jawaban atau langkah penyelesaian lengkap (+10 poin)..."></textarea>

                <!-- KOTAK PRATINJAU GAMBAR DENGAN TOMBOL HAPUS -->
                <div id="replyImgPreviewContainer_${q.id}" style="display:none; margin-bottom: 12px; position: relative; width: fit-content; background: #f1f5f9; padding: 6px; border-radius: 10px; border: 1px solid #cbd5e1;">
                  <img id="replyImgPreview_${q.id}" src="" style="max-height: 160px; border-radius: 6px; display: block; object-fit: contain;">
                  <button type="button" onclick="clearReplyImage('${q.id}')" title="Hapus Gambar Lampiran" style="position: absolute; top: -8px; right: -8px; background: #ef4444; color: white; border: none; border-radius: 50%; width: 22px; height: 22px; cursor: pointer; font-size: 12px; font-weight: bold; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">&times;</button>
                </div>

                <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px;">
                  <!-- TOMBOL UPLOAD GAMBAR KHUSUS PENJAWAB -->
                  <div>
                    <label for="replyFile_${q.id}" class="btn-reply-upload">
                      📷 <span>Lampirkan Foto Jawaban</span>
                    </label>
                    <input type="file" id="replyFile_${q.id}" accept="image/*" style="display: none;" onchange="previewReplyImage(event, '${q.id}')">
                  </div>

                  <button class="btn-login" style="width: auto; padding: 9px 20px; margin: 0; font-size: 13px;" onclick="submitReply('${q.id}', this)">Kirim Jawaban</button>
                </div>
              </div>

            </div>
          </div>
        `;
      }).join('');
    }

    function renderLeaderboard() {
      const container = document.getElementById('leaderboardContainer');
      const sorted = [...localUsers].sort((a,b) => (b.points || 0) - (a.points || 0)).slice(0, 5);

      if(sorted.length === 0) {
        container.innerHTML = `<p class="empty-sidebar-text">Belum ada peringkat harian. Mulai menjawab pertanyaan!</p>`;
        return;
      }

      const medals = ['🥇', '🥈', '🥉', '4.', '5.'];
      container.innerHTML = sorted.map((u, i) => `
        <li class="leaderboard-item">
          <div class="leaderboard-user">
            <span>${medals[i]}</span>
            <img src="${u.avatarSrc || ''}">
            <span>${escapeHtml(u.nama)}</span>
          </div>
          <div class="leaderboard-pts">${u.points || 0} pts</div>
        </li>
      `).join('');
    }
  </script>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(HTML_CONTENT)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=True)