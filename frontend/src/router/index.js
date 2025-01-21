import {createRouter, createWebHistory} from 'vue-router';

import LoginPage from "@/components/accounts/LoginPage.vue";
import CommentList from "@/components/Comments/CommentList.vue";
import RegisterPage from "@/components/accounts/RegisterPage.vue";


function isAuthenticated() {
    return !!localStorage.getItem('token'); //
}

const routes = [
    {
        path: '/',
        redirect: '/comments',
    },
    {
        path: '/login',
        name: 'login',
        component: LoginPage,
    },
    {
        path: '/comments',
        name: 'comments',
        component: CommentList,
    },
    {
        path: '/register',
        name: 'Register',
        component: RegisterPage,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;