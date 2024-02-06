import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import history from 'connect-history-api-fallback';
// https://vitejs.dev/config/

export default defineConfig({
  plugins: [svelte()],
  server: {
    middlewareMode: 'html',
    middlewares: history()
  }
});
