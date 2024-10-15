export const iconbuttonTheme = {
    base: `inline-flex items-center justify-center focus:outline-none`,
    sizes: {
      small: `p-1 rounded-2 text-xl leading-5`,
      normal: `p-1 rounded-8 text-xl leading-5`,
      large: `p-2 rounded-xl text-2xl leading-5`,
    },
    variants: {
      normal: `border border-transparent hover:border-kilvish-200 hover:bg-kilvish-200 active:border-kilvish-200 active:bg-kilvish-200 text-kilvish`,
      bordered: `border border-kilvish-300 hover:bg-kilvish-200 active:border-kilvish-200 active:bg-kilvish-200 text-kilvish`,
      disabled: `border hover:border-kilvish-200 text-kilvish-400 cursor-default`,
      active: `border border-kilvish bg-kilvish text-white shadow-key`,
    },
  }
  
  export const buttonTheme = {
    base: `inline-flex items-center focus:outline-none font-medium uppercase`,
    sizes: {
      small: `px-10 py-6 rounded-6 text-captionsm`,
      normal: `px-12 py-8 rounded-8 text-xs`,
      large: `px-14 py-12 rounded-xl text-base`,
    },
    variants: {
      primary: `border border-kilvish text-white bg-kilvish hover:border-kilvish-900 hover:bg-kilvish-900 focus:border-kilvish-800 focus:bg-kilvish-800`,
      secondary: `text-kilvish border border-kilvish-300 hover:border-kilvish-200 hover:bg-kilvish-200 active:border-kilvish-300 active:bg-kilvish-300`,
      success: `border border-green text-white bg-green hover:border-green-600 hover:bg-green-600 focus:border-green-700 focus:bg-green-700`,
      disabled: `border border-kilvish-200 text-kilvish-500 bg-kilvish-200 cursor-default`,
    },
  }
  
  export default {}
  