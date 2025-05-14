import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
// import { appStore} from './app/store'
import { appStore } from './app/store.js'
import { Provider } from 'react-redux'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider store={appStore}>
      <App />
       {/* <Toaster /> */}
    </Provider>
  </StrictMode>,
)
