/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./website/templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        current: "currentColor",
        "backgroundMenu": "#31363F",
        "navBarColor" : "#222831",
        "adminColor": "#76ABAE",
        "adminColorHover": "#558d90",
        "adminTeamTableColor": "#EEEEEE",
        "adminTeamTableContentLight": "#cfe2e3",
        "adminTeamTableContentDark": "#afced0",
        "contestLeft": "#7a7e83",
        "contestLeftTableHead": "#646970",
        "contestLeftTableOdd": "#4c4d52",
        "contestLeftTableEven": "#585b60",
        "contestRight": "#476768",
      },
    },

  },
  plugins: [],
}

