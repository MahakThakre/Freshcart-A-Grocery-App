import { createStore } from "vuex";

export default createStore({
  state: {
    currentUser: null,
    currentUserId: null,
    currentUserEmail: null,
    currentUsername: null,
    currentUserRoles: [],
  },
  mutations: {
    setCurrentUser(state, user) {
      state.currentUser = user;
      state.currentUserEmail = user.email;
      state.currentUserId = user.id;
      state.currentUsername = user.username;
      state.currentUserRoles = user.roles;
    },
  },
});
