(this.webpackJsonpclient_view=this.webpackJsonpclient_view||[]).push([[0],{24:function(e,t,c){},25:function(e,t,c){},36:function(e,t,c){"use strict";c.r(t);var n=c(1),r=c.n(n),s=c(18),i=c.n(s),a=(c(24),c(4)),j=(c(25),c(11)),u=c(2),d=c(8),l=c.n(d),b=c(9),h=c(17),o=c(0);var x=function(e){var t=e.exercise,c=e.onDelete,n=e.onEdit;return Object(o.jsxs)("tr",{children:[Object(o.jsx)("td",{children:t.name}),Object(o.jsx)("td",{children:t.reps}),Object(o.jsx)("td",{children:t.weight}),Object(o.jsx)("td",{children:t.unit}),Object(o.jsx)("td",{children:t.date}),Object(o.jsx)("td",{children:Object(o.jsx)(h.b,{className:"EditIcon",onClick:function(){return n(t)}})}),Object(o.jsx)("td",{children:Object(o.jsx)(h.a,{className:"DeleteIcon",onClick:function(){return c(t._id)}})})]})};var O=function(e){var t=e.exercises,c=e.onDelete,n=e.onEdit;return Object(o.jsxs)("table",{children:[Object(o.jsx)("thead",{children:Object(o.jsxs)("tr",{children:[Object(o.jsx)("th",{children:"Name"}),Object(o.jsx)("th",{children:"Reps"}),Object(o.jsx)("th",{children:"Weight"}),Object(o.jsx)("th",{children:"Unit"}),Object(o.jsx)("th",{children:"Date"}),Object(o.jsx)("th",{className:"BlankColumn"}),Object(o.jsx)("th",{className:"BlankColumn"})]})}),Object(o.jsx)("tbody",{children:t.map((function(e,t){return Object(o.jsx)(x,{exercise:e,onDelete:c,onEdit:n},t)}))})]})};var p=function(e){var t=e.setExerciseToEdit,c=Object(n.useState)([]),r=Object(a.a)(c,2),s=r[0],i=r[1],d=Object(u.e)(),h=function(){var e=Object(b.a)(l.a.mark((function e(t){var c;return l.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,fetch("/exercises/".concat(t),{method:"DELETE"});case 2:204===(c=e.sent).status?i(s.filter((function(e){return e._id!==t}))):console.error("Failed to delete the exercise with _id = ".concat(t,". Status code ").concat(c.status,"."));case 4:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),x=function(){var e=Object(b.a)(l.a.mark((function e(){var t,c;return l.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,fetch("/exercises");case 2:return t=e.sent,e.next=5,t.json();case 5:c=e.sent,i(c);case 7:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return Object(n.useEffect)((function(){x()}),[]),Object(o.jsxs)(o.Fragment,{children:[Object(o.jsx)("h2",{children:"Exercise Tracker App"}),Object(o.jsx)(O,{exercises:s,onDelete:h,onEdit:function(e){t(e),d.push("/edit-exercise")}}),Object(o.jsx)(j.b,{to:"/create-exercise",children:"Add Exercise"})]})};var f=function(){var e=Object(n.useState)(""),t=Object(a.a)(e,2),c=t[0],r=t[1],s=Object(n.useState)(""),i=Object(a.a)(s,2),j=i[0],d=i[1],h=Object(n.useState)(""),x=Object(a.a)(h,2),O=x[0],p=x[1],f=Object(n.useState)(""),v=Object(a.a)(f,2),g=v[0],m=v[1],y=Object(n.useState)(""),S=Object(a.a)(y,2),C=S[0],E=S[1],k=Object(u.e)(),w=function(){var e=Object(b.a)(l.a.mark((function e(){var t,n;return l.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t={name:c,reps:j,weight:O,unit:g,date:C},e.next=3,fetch("/exercises",{method:"POST",body:JSON.stringify(t),headers:{"Content-Type":"application/json"}});case 3:201===(n=e.sent).status?(alert("Successfully added the exercise."),k.push("/")):Object.values(n.body).length<5?alert("Field inputs are incorrect. Supply correct inputs to all fields."):alert("Failed to add exercise. Status code ".concat(n.status));case 5:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return Object(o.jsxs)("div",{children:[Object(o.jsx)("h1",{children:"Add Exercise"}),Object(o.jsxs)("table",{id:"exercises",children:[Object(o.jsx)("thead",{children:Object(o.jsxs)("tr",{children:[Object(o.jsx)("th",{children:"Name"}),Object(o.jsx)("th",{children:"Reps"}),Object(o.jsx)("th",{children:"Weight"}),Object(o.jsx)("th",{children:"Unit"}),Object(o.jsx)("th",{children:"Date"})]})}),Object(o.jsx)("tbody",{children:Object(o.jsxs)("tr",{className:"ModifyRow",children:[Object(o.jsx)("td",{children:Object(o.jsx)("input",{type:"text",value:c,onChange:function(e){return r(e.target.value)}})}),Object(o.jsx)("td",{children:Object(o.jsx)("input",{type:"number",value:j,onChange:function(e){return d(e.target.value)}})}),Object(o.jsx)("td",{children:Object(o.jsx)("input",{type:"Number",value:O,onChange:function(e){return p(e.target.value)}})}),Object(o.jsx)("td",{children:Object(o.jsxs)("select",{defaultValue:"blank",onChange:function(e){return m(e.target.value)},children:[Object(o.jsx)("option",{value:"blank",disabled:!0,hidden:!0,children:"Select"}),Object(o.jsx)("option",{value:"lbs",children:"lbs"}),Object(o.jsx)("option",{value:"kgs",children:"kgs"})]})}),Object(o.jsx)("td",{children:Object(o.jsx)("input",{type:"text",value:C,onChange:function(e){return E(e.target.value)}})})]})})]}),Object(o.jsx)("br",{}),Object(o.jsx)("button",{onClick:w,children:"Save"})]})};var v=function(e){var t=e.unit,c=e.setUnit;return Object(o.jsx)(o.Fragment,{children:Object(o.jsxs)("select",{defaultValue:t,onChange:function(e){return c(e.target.value)},children:[Object(o.jsx)("option",{value:"lbs",children:"lbs"}),Object(o.jsx)("option",{value:"kgs",children:"kgs"})]})})};var g=function(e){var t=e.exerciseToEdit,c=Object(n.useState)(t.name),r=Object(a.a)(c,2),s=r[0],i=r[1],j=Object(n.useState)(t.reps),d=Object(a.a)(j,2),h=d[0],x=d[1],O=Object(n.useState)(t.weight),p=Object(a.a)(O,2),f=p[0],g=p[1],m=Object(n.useState)(t.unit),y=Object(a.a)(m,2),S=y[0],C=y[1],E=Object(n.useState)(t.date),k=Object(a.a)(E,2),w=k[0],N=k[1],T=Object(u.e)(),D=function(){var e=Object(b.a)(l.a.mark((function e(){var c,n;return l.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return c={name:s,reps:h,weight:f,unit:S,date:w},e.next=3,fetch("exercises/".concat(t._id),{method:"PUT",body:JSON.stringify(c),headers:{"Content-Type":"application/json"}});case 3:200===(n=e.sent).status?(alert("Successfully edited the exercise."),T.push("/")):alert("Failed to edit exercise. Status code ".concat(n.status));case 5:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return Object(o.jsxs)("div",{children:[Object(o.jsx)("h1",{children:"Edit Exercise"}),Object(o.jsxs)("table",{id:"exercises",children:[Object(o.jsx)("thead",{children:Object(o.jsxs)("tr",{children:[Object(o.jsx)("th",{children:"Name"}),Object(o.jsx)("th",{children:"Reps"}),Object(o.jsx)("th",{children:"Weight"}),Object(o.jsx)("th",{children:"Unit"}),Object(o.jsx)("th",{children:"Date"})]})}),Object(o.jsx)("tbody",{children:Object(o.jsxs)("tr",{className:"ModifyRow",children:[Object(o.jsx)("td",{children:Object(o.jsx)("input",{type:"text",value:s,onChange:function(e){return i(e.target.value)}})}),Object(o.jsx)("td",{children:Object(o.jsx)("input",{type:"number",value:h,onChange:function(e){return x(e.target.value)}})}),Object(o.jsx)("td",{children:Object(o.jsx)("input",{type:"Number",value:f,onChange:function(e){return g(e.target.value)}})}),Object(o.jsx)("td",{children:Object(o.jsx)(v,{unit:S,setUnit:C})}),Object(o.jsx)("td",{children:Object(o.jsx)("input",{type:"text",value:w,onChange:function(e){return N(e.target.value)}})})]})})]}),Object(o.jsx)("br",{}),Object(o.jsx)("button",{onClick:D,children:"Save"})]})};var m=function(){var e=Object(n.useState)(),t=Object(a.a)(e,2),c=t[0],r=t[1];return Object(o.jsx)("div",{className:"App",children:Object(o.jsx)(j.a,{children:Object(o.jsxs)("header",{className:"App-header",children:[Object(o.jsx)(u.a,{path:"/",exact:!0,children:Object(o.jsx)(p,{setExerciseToEdit:r})}),Object(o.jsx)(u.a,{path:"/create-exercise",children:Object(o.jsx)(f,{})}),Object(o.jsx)(u.a,{path:"/edit-exercise",children:Object(o.jsx)(g,{exerciseToEdit:c})})]})})})},y=function(e){e&&e instanceof Function&&c.e(3).then(c.bind(null,37)).then((function(t){var c=t.getCLS,n=t.getFID,r=t.getFCP,s=t.getLCP,i=t.getTTFB;c(e),n(e),r(e),s(e),i(e)}))};i.a.render(Object(o.jsx)(r.a.StrictMode,{children:Object(o.jsx)(m,{})}),document.getElementById("root")),y()}},[[36,1,2]]]);
//# sourceMappingURL=main.79e2cbb3.chunk.js.map