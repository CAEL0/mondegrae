const Dashboard = () => import('@/layouts/Dashboard');
const DashboardHome = () => import('@/pages/Home');
const NotFound = () => import('@/pages/NotFound');

export default [
  { path: '/', component: Dashboard,
    children: [
      { path: '/', name: 'DashboardHome', component: DashboardHome }
    ]
  },
  { path: "*", component: NotFound }
]