
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        beforeEnter() {
          if (typeof window !== 'undefined') {
            window.location.href = 'https://globalsecuritydatabase.org';
          }
        },
      },
      { path: 'home', component: () => import('pages/Index.vue') },
      { path: ':id(GSD-\\d{4}-\\d{4,})', component: () => import('pages/Identifier.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
