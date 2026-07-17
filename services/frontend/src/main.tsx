import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import '@fontsource/epilogue/400.css'
import '@fontsource/epilogue/500.css'
import '@fontsource/epilogue/600.css'
import '@fontsource/epilogue/700.css'
import '@fontsource/space-grotesk/500.css'
import '@fontsource/space-grotesk/700.css'
import './index.css'
import App from './App'
import { AuthProvider } from './auth/auth-context'
import { GameProvider } from './game-context'
import { ThemeProvider } from './theme-context'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <AuthProvider>
        <GameProvider>
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </GameProvider>
      </AuthProvider>
    </ThemeProvider>
  </StrictMode>
)
