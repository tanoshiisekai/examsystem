import Vue from "vue";
import Router from "vue-router";
import Login from "@/components/Login";
import Register from "@/components/Register";
import AdminLogin from "@/components/AdminLogin";
import AddProblem1 from "@/components/AddProblem1";
import AddProblem2_1 from "@/components/AddProblem2_1";
import AddProblem2_2 from "@/components/AddProblem2_2";
import ManageSet from "@/components/ManageSet";
import AdminSettings from "@/components/AdminSettings";
import Problems from "@/components/Problems";
import UserSettings from "@/components/UserSettings";
import AnswerProblems from "@/components/AnswerProblems";



Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "login",
      component: Login
    },
    {
      path: "/register",
      name: "register",
      component: Register
    },
    {
      path: "/adminlogin",
      name: "adminlogin",
      component: AdminLogin
    },
    {
      path: "/addproblem1",
      name: "addproblem1",
      component: AddProblem1
    },
    {
      path: "/addproblem2_1",
      name: "addproblem2_1",
      component: AddProblem2_1
    },
    {
      path: "/addproblem2_2",
      name: "addproblem2_2",
      component: AddProblem2_2
    },
    {
      path: "/manageset",
      name: "manageset",
      component: ManageSet
    },
    {
      path: "/adminsettings",
      name: "adminsettings",
      component: AdminSettings
    },
    {
      path: "/problems",
      name: "problems",
      component: Problems
    },
    {
      path: "/usersettings",
      name: "usersettings",
      component: UserSettings
    },
    {
      path: "/answerproblems",
      name: "answerproblems",
      component: AnswerProblems
    }
  ]
});
