import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    user: {
      token: '',
      isAuthenticated: false
    }
  },
  mutations: {
    initializeStore(state) {
      const token = localStorage.getItem('token')
      if (token) {
        state.user.token = token
        state.user.isAuthenticated = true
        axios.defaults.headers.common['Authorization'] = 'Token ' + token
      } else {
        state.user.token = ''
        state.user.isAuthenticated = false
        delete axios.defaults.headers.common['Authorization']
      }
    },
    setToken(state, token) {
      state.user.token = token
      state.user.isAuthenticated = true
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = 'Token ' + token
    },
    removeToken(state) {
      state.user.token = ''
      state.user.isAuthenticated = false
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})
