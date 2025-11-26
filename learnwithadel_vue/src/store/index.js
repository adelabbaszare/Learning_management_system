import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    user: {
      token: '',
      isAuthenticated: false,
      username: '',
      is_instructor: false,
      email: '',
      image: '',
      first_name: '',
      last_name: '',
      bio: '',
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
    setUserData(state, userData) {
        state.user.username = userData.username;
        state.user.is_instructor = userData.is_instructor;
        state.user.email = userData.email;
        state.user.image = userData.image;
        state.user.first_name = userData.first_name;
        state.user.last_name = userData.last_name;
        state.user.bio = userData.bio;
    },
    removeToken(state) {
      state.user.token = ''
      state.user.isAuthenticated = false
      state.user.username = '';
      state.user.is_instructor = false;
      state.user.email = '';
      state.user.image = '';
      state.user.first_name = '';
      state.user.last_name = '';
      state.user.bio = '';
      
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})