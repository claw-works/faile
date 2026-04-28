<template>
  <div id="app">
    <nav>
      <router-link to="/">🖼️ 图片处理</router-link>
      <router-link to="/doc">📄 文档转换</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: #f5f5f5; color: #333; }
#app { max-width: 1200px; margin: 0 auto; padding: 20px; }
nav { display: flex; gap: 16px; margin-bottom: 24px; padding: 12px 0; border-bottom: 2px solid #e0e0e0; }
nav a { text-decoration: none; color: #666; font-weight: 500; padding: 6px 12px; border-radius: 6px; }
nav a.router-link-active { background: #4f46e5; color: white; }
</style>
