import os, textwrap

BASE = r'F:\PROJECTS\PROJECTS-DJANGO\POLLING-DJANGO\poll_portal\templates\poll_portal'

def w(name, content):
    with open(os.path.join(BASE, name), 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {name}')

# =========== base.html ===========
w('base.html', """\
{%% load static %%}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{%% block title %%}VoteSphere{%% endblock %%} | VoteSphere</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
  <style>
    body{background:#f0f2f5;font-family:'Segoe UI',sans-serif;color:#1a1a2e;min-height:100vh;display:flex;flex-direction:column;}
    .navbar{background:linear-gradient(135deg,#6366f1,#8b5cf6,#a855f7)!important;box-shadow:0 4px 20px rgba(99,102,241,.4);padding:.8rem 0;}
    .navbar-brand{font-weight:800;font-size:1.35rem;color:#fff!important;}
    .navbar-brand i{color:#fde68a;}
    .navbar .nav-link{color:rgba(255,255,255,.85)!important;font-weight:500;padding:.4rem .9rem!important;border-radius:8px;transition:all .2s;}
    .navbar .nav-link:hover{color:#fff!important;background:rgba(255,255,255,.15);}
    .badge-admin{background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;font-size:.72rem;padding:3px 8px;border-radius:20px;font-weight:600;}
    .card{border:none;border-radius:20px;box-shadow:0 2px 16px rgba(0,0,0,.07);transition:box-shadow .25s,transform .2s;}
    .card:hover{box-shadow:0 8px 32px rgba(0,0,0,.12);}
    .card-header{border-radius:20px 20px 0 0!important;border-bottom:none;padding:1.3rem 1.6rem;}
    .card-header-gradient{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;}
    .card-header-dark{background:linear-gradient(135deg,#1e1b4b,#312e81);color:#fff;}
    .card-footer{background:#f8fafc;border-top:1px solid #f1f5f9;border-radius:0 0 20px 20px!important;padding:1rem 1.6rem;}
    .btn{font-weight:500;font-size:.875rem;border-radius:10px;transition:all .2s;}
    .btn-primary{background:linear-gradient(135deg,#6366f1,#8b5cf6);border:none;box-shadow:0 4px 14px rgba(99,102,241,.3);}
    .btn-primary:hover{background:linear-gradient(135deg,#4f46e5,#7c3aed);transform:translateY(-1px);}
    .btn-success{background:linear-gradient(135deg,#10b981,#059669);border:none;}
    .btn-success:hover{transform:translateY(-1px);}
    .btn-danger{background:linear-gradient(135deg,#ef4444,#dc2626);border:none;}
    .btn-danger:hover{transform:translateY(-1px);}
    .btn-warning{background:linear-gradient(135deg,#f59e0b,#d97706);border:none;color:#fff;}
    .btn-outline-primary{border:1.5px solid #6366f1;color:#6366f1;}
    .btn-outline-primary:hover{background:#6366f1;color:#fff;}
    .btn-outline-secondary{border:1.5px solid #cbd5e1;color:#64748b;}
    .btn-outline-secondary:hover{background:#f1f5f9;color:#334155;}
    .btn-outline-success{border:1.5px solid #10b981;color:#059669;}
    .btn-outline-success:hover{background:#d1fae5;}
    .btn-outline-danger{border:1.5px solid #ef4444;color:#dc2626;}
    .btn-outline-danger:hover{background:#fee2e2;}
    .btn-outline-warning{border:1.5px solid #f59e0b;color:#d97706;}
    .btn-outline-warning:hover{background:#fef3c7;}
    .form-control,.form-select{border-radius:10px;border:1.5px solid #e2e8f0;padding:.65rem 1rem;font-size:.9rem;transition:border-color .2s,box-shadow .2s;}
    .form-control:focus,.form-select:focus{border-color:#6366f1;box-shadow:0 0 0 3px rgba(99,102,241,.15);outline:none;}
    .input-group-text{border-radius:10px 0 0 10px;border:1.5px solid #e2e8f0;border-right:none;background:#f8fafc;color:#64748b;}
    .input-group .form-control{border-radius:0 10px 10px 0;}
    .form-label{font-weight:600;font-size:.85rem;color:#374151;margin-bottom:.4rem;}
    .alert{border-radius:14px;border:none;font-size:.875rem;font-weight:500;}
    .alert-success{background:#d1fae5;color:#065f46;}
    .alert-danger{background:#fee2e2;color:#991b1b;}
    .alert-warning{background:#fef3c7;color:#92400e;}
    .alert-info{background:#dbeafe;color:#1e40af;}
    .hero-section{background:linear-gradient(135deg,#6366f1,#8b5cf6,#a855f7);color:#fff;padding:3.5rem 0 3rem;margin-bottom:2.5rem;border-radius:0 0 40px 40px;position:relative;overflow:hidden;}
    .hero-section::before{content:'';position:absolute;top:-60px;right:-60px;width:300px;height:300px;background:rgba(255,255,255,.06);border-radius:50%;}
    .poll-card{transition:transform .2s,box-shadow .2s;}
    .poll-card:hover{transform:translateY(-4px)!important;box-shadow:0 12px 40px rgba(99,102,241,.15)!important;}
    .option-dot{width:8px;height:8px;background:#6366f1;border-radius:50%;display:inline-block;margin-right:8px;flex-shrink:0;margin-top:5px;}
    .progress{border-radius:30px;height:24px;background:#f1f5f9;overflow:hidden;}
    .progress-bar{display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700;border-radius:30px;transition:width .6s ease;}
    .winner-badge{background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;border-radius:20px;padding:3px 10px;font-size:.72rem;font-weight:700;display:inline-flex;align-items:center;gap:3px;}
    .vote-option{cursor:pointer;border:2px solid #e8ecef;border-radius:14px;padding:1rem 1.2rem;transition:all .2s;background:#fff;user-select:none;display:flex;align-items:center;gap:.75rem;}
    .vote-option:hover{border-color:#6366f1;background:#faf5ff;}
    .vote-option input[type=radio]{accent-color:#6366f1;width:1.1em;height:1.1em;}
    .stat-card{border-radius:20px;padding:1.8rem;background:#fff;box-shadow:0 2px 16px rgba(0,0,0,.07);text-align:center;}
    .stat-number{font-size:2.8rem;font-weight:800;line-height:1;margin-bottom:.3rem;}
    .stat-label{font-size:.8rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:#94a3b8;}
    .table{font-size:.875rem;}
    .table th{font-weight:600;color:#64748b;text-transform:uppercase;font-size:.72rem;letter-spacing:.05em;border-bottom:2px solid #f1f5f9;}
    .table td{vertical-align:middle;border-color:#f8fafc;}
    .divider{height:1px;background:linear-gradient(to right,transparent,#e2e8f0,transparent);margin:1.5rem 0;}
    footer{background:linear-gradient(135deg,#1e1b4b,#312e81);color:#a5b4fc;padding:2rem 0;margin-top:auto;}
  </style>
</head>
<body>
<nav class="navbar navbar-expand-lg">
  <div class="container">
    <a class="navbar-brand" href="{%% url 'home' %%}"><i class="bi bi-bar-chart-line-fill"></i> VoteSphere</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
      <span class="navbar-toggler-icon" style="filter:invert(1)"></span>
    </button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0 gap-1">
        <li class="nav-item"><a class="nav-link" href="{%% url 'home' %%}"><i class="bi bi-house-door me-1"></i>Home</a></li>
        {%% if user.is_authenticated and user.is_staff %%}
        <li class="nav-item"><a class="nav-link" href="{%% url 'create' %%}"><i class="bi bi-plus-circle me-1"></i>Create Poll</a></li>
        <li class="nav-item"><a class="nav-link" href="{%% url 'admin_dashboard' %%}"><i class="bi bi-speedometer2 me-1"></i>Dashboard</a></li>
        <li class="nav-item"><a class="nav-link" href="{%% url 'admin:index' %%}"><i class="bi bi-gear me-1"></i>Admin Panel</a></li>
        {%% endif %%}
      </ul>
      <ul class="navbar-nav ms-auto align-items-center gap-1">
        {%% if user.is_authenticated %%}
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle d-flex align-items-center gap-2" href="#" data-bs-toggle="dropdown">
            <span style="width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,.22);display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:.9rem;">{%% spaceless %%}{{ user.username|first|upper }}{%% endspaceless %%}</span>
            <span>{{ user.username }}</span>
            {%% if user.is_staff %%}<span class="badge-admin">Admin</span>{%% endif %%}
          </a>
          <ul class="dropdown-menu dropdown-menu-end shadow border-0" style="border-radius:14px;">
            <li><a class="dropdown-item text-danger d-flex gap-2 align-items-center" href="{%% url 'logout' %%}"><i class="bi bi-box-arrow-right"></i>Logout</a></li>
          </ul>
        </li>
        {%% else %%}
        <li class="nav-item"><a class="nav-link" href="{%% url 'login' %%}"><i class="bi bi-box-arrow-in-right me-1"></i>Login</a></li>
        <li class="nav-item"><a href="{%% url 'register' %%}" class="btn btn-sm ms-1" style="background:rgba(255,255,255,.18);color:#fff;border:1.5px solid rgba(255,255,255,.35);border-radius:10px;font-weight:600;padding:.4rem 1rem;"><i class="bi bi-person-plus me-1"></i>Register</a></li>
        {%% endif %%}
      </ul>
    </div>
  </div>
</nav>
<div style="flex:1;">
  <div class="container mt-4">
    {%% for message in messages %%}
    <div class="alert alert-{{ message.tags }} alert-dismissible fade show d-flex align-items-center gap-2" role="alert">
      {%% if message.tags == 'success' %%}<i class="bi bi-check-circle-fill fs-5"></i>
      {%% elif message.tags == 'danger' %%}<i class="bi bi-x-circle-fill fs-5"></i>
      {%% elif message.tags == 'warning' %%}<i class="bi bi-exclamation-triangle-fill fs-5"></i>
      {%% else %%}<i class="bi bi-info-circle-fill fs-5"></i>{%% endif %%}
      <span>{{ message }}</span>
      <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
    </div>
    {%% endfor %%}
    {%% block main %%}{%% endblock %%}
  </div>
</div>
<footer class="mt-5">
  <div class="container text-center">
    <div style="font-size:1.4rem;margin-bottom:.3rem;"><i class="bi bi-bar-chart-line-fill" style="color:#fde68a;"></i></div>
    <div style="font-weight:700;font-size:1rem;color:#e0e7ff;">VoteSphere</div>
    <div style="font-size:.82rem;margin-top:.3rem;">Secure, Simple, Fair Elections</div>
  </div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""" % {})

print('Done base.html')
