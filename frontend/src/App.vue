<template>
  <div id="app">
    <header class="site-header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-mark">✦</span>
          <span class="logo-text">faile</span>
        </div>
        <p class="slogan">Turn files into fuel for AI</p>
        <nav class="nav">
          <router-link to="/">🖼️ 图片处理</router-link>
          <router-link to="/doc">📄 文档转换</router-link>
        </nav>
      </div>
    </header>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #f0f2f5;
  color: #1a1a2e;
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ── Header ── */
.site-header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
  color: white;
  padding: 28px 24px 0;
  box-shadow: 0 2px 20px rgba(0,0,0,0.2);
}
.header-inner {
  max-width: 1100px;
  margin: 0 auto;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.logo-mark {
  font-size: 22px;
  color: #e94560;
  line-height: 1;
}
.logo-text {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(90deg, #fff 0%, #a8b8ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.slogan {
  font-size: 13px;
  color: rgba(255,255,255,0.5);
  margin-bottom: 20px;
  letter-spacing: 0.3px;
}

/* ── Nav tabs ── */
.nav {
  display: flex;
  gap: 4px;
}
.nav a {
  text-decoration: none;
  color: rgba(255,255,255,0.6);
  font-size: 14px;
  font-weight: 500;
  padding: 10px 18px;
  border-radius: 8px 8px 0 0;
  transition: all 0.15s;
}
.nav a:hover { color: white; background: rgba(255,255,255,0.08); }
.nav a.router-link-active {
  color: #1a1a2e;
  background: #f0f2f5;
  font-weight: 600;
}

/* ── Main ── */
.main-content {
  flex: 1;
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
  padding: 28px 24px;
}
</style>
