import {
  AccentColor,
  AnimationScene,
  AnimationType,
  BackgroundColor,
  BodyFont,
  BodyTextSize,
  BorderColor,
  FramingOption,
  HeadingFont,
  HeadingFontWeight,
  HeadingSize,
  LayoutConfiguration,
  LayoutType,
  LetterSpacing,
  Shadow,
  StyleOption,
  SubHeadingSize,
  ThemeOption,
  TypefaceOption
} from '@/lib/types'
  
  // ================================
  // WEB LAYOUT TYPES
  // ================================
  
  export const WEB_LAYOUT_TYPES: LayoutType[] = [
    {
      "name": "Hero",
      "prompt": "Create a hero layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 space-y-2'><div class='h-3 bg-gray-300 rounded w-3/4 mx-auto'></div><div class='h-2 bg-gray-200 rounded w-1/2 mx-auto'></div><div class='h-2 bg-gray-200 rounded w-2/3 mx-auto'></div><div class='flex gap-2 justify-center mt-3'><div class='h-2 w-8 bg-gray-400 rounded'></div><div class='h-2 w-8 bg-gray-300 rounded'></div></div></div>"
    },
    {
      "name": "Features",
      "prompt": "Create a features layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3'><div class='grid grid-cols-3 gap-2 h-full'><div class='bg-gray-200 rounded flex flex-col gap-1 p-2'><div class='w-3 h-3 bg-gray-300 rounded'></div><div class='h-1 bg-gray-300 rounded'></div><div class='h-1 bg-gray-250 rounded w-3/4'></div></div><div class='bg-gray-200 rounded flex flex-col gap-1 p-2'><div class='w-3 h-3 bg-gray-300 rounded'></div><div class='h-1 bg-gray-300 rounded'></div><div class='h-1 bg-gray-250 rounded w-3/4'></div></div><div class='bg-gray-200 rounded flex flex-col gap-1 p-2'><div class='w-3 h-3 bg-gray-300 rounded'></div><div class='h-1 bg-gray-300 rounded'></div><div class='h-1 bg-gray-250 rounded w-3/4'></div></div></div></div>"
    },
    {
      "name": "Onboarding",
      "prompt": "Create an onboarding layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 flex flex-col items-center justify-center space-y-2'><div class='w-8 h-8 bg-gray-200 rounded'></div><div class='h-1.5 bg-gray-300 rounded w-2/3'></div><div class='flex gap-1'><div class='w-1.5 h-1.5 bg-gray-300 rounded-full'></div><div class='w-1.5 h-1.5 bg-gray-300 rounded-full'></div><div class='w-1.5 h-1.5 bg-gray-400 rounded-full'></div></div></div>"
    },
    {
      "name": "Docs",
      "prompt": "Create a docs layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-2'><div class='w-1/4 bg-gray-200 rounded p-2 space-y-1'><div class='h-1 bg-gray-300 rounded'></div><div class='h-1 bg-gray-300 rounded'></div><div class='h-1 bg-gray-300 rounded w-3/4'></div></div><div class='flex-1 bg-gray-200 rounded p-2 space-y-1'><div class='h-1.5 bg-gray-300 rounded w-3/4'></div><div class='h-1 bg-gray-250 rounded'></div><div class='h-1 bg-gray-250 rounded w-5/6'></div></div></div>"
    },
    {
      "name": "Updates",
      "prompt": "Create an updates layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3 space-y-2'><div class='bg-gray-200 rounded p-2 space-y-1'><div class='h-1.5 bg-gray-300 rounded w-2/3'></div><div class='h-1 bg-gray-250 rounded'></div></div><div class='bg-gray-200 rounded p-2 space-y-1'><div class='h-1.5 bg-gray-300 rounded w-1/2'></div><div class='h-1 bg-gray-250 rounded w-4/5'></div></div></div>"
    },
    {
      "name": "Portfolio",
      "prompt": "Create a portfolio layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='grid grid-cols-3 gap-1 h-full'><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div></div></div>"
    },
    {
      "name": "Pricing",
      "prompt": "Create a pricing layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='grid grid-cols-3 gap-1 h-full'><div class='bg-gray-200 rounded flex flex-col items-center justify-center gap-1 p-1'><div class='h-1 bg-gray-300 rounded w-1/2'></div><div class='text-xs text-gray-400'>$</div><div class='h-1 bg-gray-300 rounded w-2/3'></div></div><div class='bg-gray-300 rounded flex flex-col items-center justify-center gap-1 p-1 border-2 border-gray-400'><div class='h-1 bg-gray-400 rounded w-1/2'></div><div class='text-xs text-gray-500'>$$</div><div class='h-1 bg-gray-400 rounded w-2/3'></div></div><div class='bg-gray-200 rounded flex flex-col items-center justify-center gap-1 p-1'><div class='h-1 bg-gray-300 rounded w-1/2'></div><div class='text-xs text-gray-400'>$</div><div class='h-1 bg-gray-300 rounded w-2/3'></div></div></div></div>"
    },
    {
      "name": "Gallery",
      "prompt": "Create a gallery layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='grid grid-cols-4 gap-1 h-full'><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div></div></div>"
    },
    {
      "name": "Dashboard",
      "prompt": "Create a dashboard layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 space-y-1'><div class='grid grid-cols-4 gap-1'><div class='h-4 bg-gray-250 rounded'></div><div class='h-4 bg-gray-250 rounded'></div><div class='h-4 bg-gray-250 rounded'></div><div class='h-4 bg-gray-250 rounded'></div></div><div class='grid grid-cols-3 gap-1 flex-1'><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div></div></div>"
    },
    {
      "name": "Login",
      "prompt": "Create a login layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 flex items-center justify-center'><div class='bg-gray-200 rounded p-3 w-3/4 space-y-1.5'><div class='h-1 bg-gray-300 rounded w-1/3'></div><div class='h-1.5 bg-gray-150 rounded border border-gray-300'></div><div class='h-1.5 bg-gray-150 rounded border border-gray-300'></div><div class='h-1.5 bg-gray-400 rounded'></div></div></div>"
    },
    {
      "name": "Email",
      "prompt": "Create an email layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 flex flex-col items-center justify-center space-y-2'><div class='h-1.5 bg-gray-300 rounded w-2/3'></div><div class='h-1 bg-gray-250 rounded w-1/2'></div><div class='flex gap-1 w-full justify-center'><div class='h-1.5 bg-gray-150 rounded border border-gray-300 flex-1 max-w-16'></div><div class='h-1.5 bg-gray-400 rounded w-8'></div></div></div>"
    },
    {
      "name": "Testimonials",
      "prompt": "Create a testimonials layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='grid grid-cols-3 gap-1 h-full'><div class='bg-gray-200 rounded p-2 space-y-1'><div class='w-2 h-2 bg-gray-300 rounded-full'></div><div class='h-1 bg-gray-250 rounded'></div><div class='h-1 bg-gray-250 rounded w-3/4'></div></div><div class='bg-gray-200 rounded p-2 space-y-1'><div class='w-2 h-2 bg-gray-300 rounded-full'></div><div class='h-1 bg-gray-250 rounded'></div><div class='h-1 bg-gray-250 rounded w-3/4'></div></div><div class='bg-gray-200 rounded p-2 space-y-1'><div class='w-2 h-2 bg-gray-300 rounded-full'></div><div class='h-1 bg-gray-250 rounded'></div><div class='h-1 bg-gray-250 rounded w-3/4'></div></div></div></div>"
    },
    {
      "name": "Payment",
      "prompt": "Create a payment layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-1'><div class='flex-1 bg-gray-200 rounded p-2 space-y-1'><div class='h-1 bg-gray-300 rounded w-1/3'></div><div class='h-1 bg-gray-150 rounded border border-gray-300'></div><div class='h-1 bg-gray-150 rounded border border-gray-300'></div><div class='grid grid-cols-2 gap-1'><div class='h-1 bg-gray-150 rounded border border-gray-300'></div><div class='h-1 bg-gray-150 rounded border border-gray-300'></div></div></div><div class='flex-1 bg-gray-200 rounded p-2 space-y-1'><div class='h-1 bg-gray-300 rounded w-1/3'></div><div class='flex-1 bg-gray-150 rounded'></div><div class='h-1 bg-gray-400 rounded'></div></div></div>"
    },
    {
      "name": "Footer",
      "prompt": "Create a footer layout",
      "html": "<div class='w-full h-24 bg-gray-200 rounded p-3'><div class='grid grid-cols-4 gap-2 h-full'><div class='space-y-1'><div class='h-1 bg-gray-300 rounded w-2/3'></div><div class='h-0.5 bg-gray-250 rounded w-1/2'></div><div class='h-0.5 bg-gray-250 rounded w-2/3'></div></div><div class='space-y-1'><div class='h-1 bg-gray-300 rounded w-2/3'></div><div class='h-0.5 bg-gray-250 rounded w-1/2'></div><div class='h-0.5 bg-gray-250 rounded w-2/3'></div></div><div class='space-y-1'><div class='h-1 bg-gray-300 rounded w-2/3'></div><div class='h-0.5 bg-gray-250 rounded w-1/2'></div><div class='h-0.5 bg-gray-250 rounded w-2/3'></div></div><div class='space-y-1'><div class='h-1 bg-gray-300 rounded w-2/3'></div><div class='h-0.5 bg-gray-250 rounded w-1/2'></div><div class='h-0.5 bg-gray-250 rounded w-2/3'></div></div></div></div>"
    },
    {
      "name": "FAQ",
      "prompt": "Create an FAQ layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3 space-y-1'><div class='bg-gray-200 rounded p-2 space-y-1'><div class='h-1.5 bg-gray-300 rounded w-2/3'></div><div class='h-1 bg-gray-250 rounded'></div></div><div class='bg-gray-200 rounded p-2 space-y-1'><div class='h-1.5 bg-gray-300 rounded w-1/2'></div><div class='h-1 bg-gray-250 rounded w-4/5'></div></div><div class='bg-gray-200 rounded p-1'><div class='h-1.5 bg-gray-300 rounded w-3/4'></div></div></div>"
    },
    {
      "name": "Explore",
      "prompt": "Create an explore layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 space-y-1'><div class='flex gap-1'><div class='h-1 bg-gray-300 rounded w-6 text-xs'></div><div class='h-1 bg-gray-300 rounded w-6'></div><div class='h-1 bg-gray-300 rounded w-8'></div></div><div class='grid grid-cols-3 gap-1 flex-1'><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div></div></div>"
    },
    {
      "name": "Settings",
      "prompt": "Create a settings layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3'><div class='bg-gray-200 rounded p-2 space-y-2'><div class='flex items-center justify-between'><div class='h-1 bg-gray-300 rounded w-1/2'></div><div class='w-3 h-1.5 bg-gray-150 rounded-full border border-gray-300 relative'><div class='absolute right-0 top-0 w-1.5 h-1.5 bg-gray-300 rounded-full'></div></div></div><div class='flex items-center justify-between'><div class='h-1 bg-gray-300 rounded w-2/3'></div><div class='h-1 bg-gray-150 rounded border border-gray-300 w-8'></div></div></div></div>"
    },
    {
      "name": "About",
      "prompt": "Create an about layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-1'><div class='flex-1 space-y-1 py-2'><div class='h-1.5 bg-gray-300 rounded w-1/2'></div><div class='h-1 bg-gray-200 rounded'></div><div class='h-1 bg-gray-200 rounded w-5/6'></div><div class='h-1 bg-gray-200 rounded w-3/4'></div></div><div class='flex-1 bg-gray-250 rounded'></div></div>"
    },
    {
      "name": "Blog",
      "prompt": "Create a blog layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 space-y-1'><div class='flex gap-1 bg-gray-200 rounded p-1.5'><div class='w-8 h-6 bg-gray-250 rounded'></div><div class='flex-1 space-y-1'><div class='h-1.5 bg-gray-300 rounded'></div><div class='h-1 bg-gray-250 rounded w-5/6'></div></div></div><div class='flex gap-1 bg-gray-200 rounded p-1.5'><div class='w-8 h-6 bg-gray-250 rounded'></div><div class='flex-1 space-y-1'><div class='h-1.5 bg-gray-300 rounded'></div><div class='h-1 bg-gray-250 rounded w-4/6'></div></div></div></div>"
    },
    {
      "name": "Video",
      "prompt": "Create a video layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3'><div class='w-full h-full bg-gray-250 rounded flex items-center justify-center'><div class='w-4 h-4 bg-gray-400 rounded-full flex items-center justify-center'><div class='w-0 h-0 border-l-2 border-l-gray-100 border-y-transparent border-y-1 border-r-0 ml-0.5'></div></div></div></div>"
    },
    {
      "name": "Landing Page",
      "prompt": "Create a landing page layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 space-y-1'><div class='text-center space-y-1 py-1'><div class='h-1.5 bg-gray-300 rounded w-2/3 mx-auto'></div><div class='h-1 bg-gray-250 rounded w-1/2 mx-auto'></div><div class='h-1 bg-gray-400 rounded w-1/4 mx-auto'></div></div><div class='grid grid-cols-3 gap-1 flex-1'><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div></div></div>"
    }
  ]

  export const MOBILE_LAYOUT_TYPES: LayoutType[] = [
    {
      "name": "Hero",
      "prompt": "Create a mobile hero layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 flex flex-col items-center justify-center space-y-2'><div class='h-2 bg-gray-300 rounded w-3/4'></div><div class='h-1.5 bg-gray-250 rounded w-1/2'></div><div class='h-1.5 bg-gray-400 rounded w-1/3 mt-2'></div></div>"
    },
    {
      "name": "Features",
      "prompt": "Create a mobile features layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3'><div class='grid grid-cols-2 gap-2 h-full'><div class='bg-gray-200 rounded p-2 space-y-1'><div class='w-3 h-3 bg-gray-300 rounded'></div><div class='h-1 bg-gray-300 rounded w-3/4'></div><div class='h-0.5 bg-gray-250 rounded'></div></div><div class='bg-gray-200 rounded p-2 space-y-1'><div class='w-3 h-3 bg-gray-300 rounded'></div><div class='h-1 bg-gray-300 rounded w-3/4'></div><div class='h-0.5 bg-gray-250 rounded'></div></div><div class='bg-gray-200 rounded p-2 space-y-1'><div class='w-3 h-3 bg-gray-300 rounded'></div><div class='h-1 bg-gray-300 rounded w-3/4'></div><div class='h-0.5 bg-gray-250 rounded'></div></div><div class='bg-gray-200 rounded p-2 space-y-1'><div class='w-3 h-3 bg-gray-300 rounded'></div><div class='h-1 bg-gray-300 rounded w-3/4'></div><div class='h-0.5 bg-gray-250 rounded'></div></div></div></div>"
    },
    {
      "name": "Onboarding",
      "prompt": "Create a mobile onboarding layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 flex flex-col items-center justify-center space-y-2'><div class='w-8 h-8 bg-gray-250 rounded-full'></div><div class='h-1.5 bg-gray-300 rounded w-2/3'></div><div class='h-1 bg-gray-250 rounded w-1/2'></div><div class='flex gap-1 mt-2'><div class='w-1.5 h-1.5 bg-gray-300 rounded-full'></div><div class='w-1.5 h-1.5 bg-gray-300 rounded-full'></div><div class='w-1.5 h-1.5 bg-gray-400 rounded-full'></div></div></div>"
    },
    {
      "name": "Dashboard",
      "prompt": "Create a mobile dashboard layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3 space-y-2'><div class='bg-gray-200 rounded p-2'><div class='h-1.5 bg-gray-300 rounded w-1/2'></div><div class='h-3 bg-gray-150 rounded mt-1'></div></div><div class='bg-gray-200 rounded p-2'><div class='h-1.5 bg-gray-300 rounded w-2/3'></div><div class='h-3 bg-gray-150 rounded mt-1'></div></div></div>"
    },
    {
      "name": "Login",
      "prompt": "Create a mobile login layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 flex items-center justify-center'><div class='w-full max-w-20 space-y-2'><div class='h-1.5 bg-gray-300 rounded w-1/3'></div><div class='h-2 bg-gray-150 rounded border border-gray-300'></div><div class='h-2 bg-gray-150 rounded border border-gray-300'></div><div class='h-2 bg-gray-400 rounded'></div></div></div>"
    },
    {
      "name": "Settings",
      "prompt": "Create a mobile settings layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3 space-y-2'><div class='bg-gray-200 rounded p-2 flex items-center justify-between'><div class='h-1 bg-gray-300 rounded w-1/2'></div><div class='w-3 h-1.5 bg-gray-150 rounded-full border border-gray-300 relative'><div class='absolute right-0 top-0 w-1.5 h-1.5 bg-gray-400 rounded-full'></div></div></div><div class='bg-gray-200 rounded p-2 flex items-center justify-between'><div class='h-1 bg-gray-300 rounded w-2/3'></div><div class='w-3 h-1.5 bg-gray-150 rounded-full border border-gray-300 relative'><div class='absolute left-0 top-0 w-1.5 h-1.5 bg-gray-300 rounded-full'></div></div></div></div>"
    },
    {
      "name": "Profile",
      "prompt": "Create a mobile profile layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 flex flex-col items-center justify-center space-y-2'><div class='w-6 h-6 bg-gray-250 rounded-full'></div><div class='h-1.5 bg-gray-300 rounded w-1/2'></div><div class='h-1 bg-gray-250 rounded w-1/3'></div><div class='h-1.5 bg-gray-400 rounded w-2/5'></div></div>"
    },
    {
      "name": "Gallery",
      "prompt": "Create a mobile gallery layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='grid grid-cols-3 gap-1 h-full'><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div></div></div>"
    },
    {
      "name": "Explore",
      "prompt": "Create a mobile explore layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 space-y-1'><div class='h-2 bg-gray-150 rounded border border-gray-300'></div><div class='grid grid-cols-2 gap-1 flex-1'><div class='bg-gray-200 rounded p-1.5'><div class='h-1 bg-gray-300 rounded w-2/3'></div><div class='h-0.5 bg-gray-250 rounded mt-1'></div></div><div class='bg-gray-200 rounded p-1.5'><div class='h-1 bg-gray-300 rounded w-2/3'></div><div class='h-0.5 bg-gray-250 rounded mt-1'></div></div></div></div>"
    },
    {
      "name": "FAQ",
      "prompt": "Create a mobile FAQ layout",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3 space-y-1'><div class='bg-gray-200 rounded p-2 space-y-1'><div class='h-1.5 bg-gray-300 rounded w-2/3'></div><div class='h-1 bg-gray-250 rounded'></div></div><div class='bg-gray-200 rounded p-2 space-y-1'><div class='h-1.5 bg-gray-300 rounded w-1/2'></div><div class='h-1 bg-gray-250 rounded w-4/5'></div></div><div class='bg-gray-200 rounded p-1.5'><div class='h-1.5 bg-gray-300 rounded w-3/4'></div></div></div>"
    }
  ]
  
  // ================================
  // LAYOUT CONFIGURATIONS
  // ================================
  
  export const LAYOUT_CONFIGURATIONS: LayoutConfiguration[] = [
    {
      "name": "Card",
      "prompt": "Layout Configuration: Card (centered content in a card container)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 flex items-center justify-center'><div class='w-16 h-12 bg-gray-250 rounded-lg border border-gray-300'></div></div>"
    },
    {
      "name": "List",
      "prompt": "Layout Configuration: List (vertically stacked items in a list format)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3 space-y-2'><div class='h-3 bg-gray-250 rounded'></div><div class='h-3 bg-gray-250 rounded'></div><div class='h-3 bg-gray-250 rounded'></div><div class='h-3 bg-gray-250 rounded'></div></div>"
    },
    {
      "name": "2-2 Square",
      "prompt": "Layout Configuration: 2-2 Square (four equal-sized cells in a square grid)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3'><div class='grid grid-cols-2 gap-2 h-full'><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div></div></div>"
    },
    {
      "name": "Table",
      "prompt": "Layout Configuration: Table (data organized in a structured grid with rows and columns)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3 flex items-center justify-center'><div class='grid grid-cols-3 gap-1'><div class='w-4 h-2 bg-gray-300 rounded-sm'></div><div class='w-4 h-2 bg-gray-300 rounded-sm'></div><div class='w-4 h-2 bg-gray-300 rounded-sm'></div><div class='w-4 h-2 bg-gray-200 rounded-sm'></div><div class='w-4 h-2 bg-gray-200 rounded-sm'></div><div class='w-4 h-2 bg-gray-200 rounded-sm'></div><div class='w-4 h-2 bg-gray-200 rounded-sm'></div><div class='w-4 h-2 bg-gray-200 rounded-sm'></div><div class='w-4 h-2 bg-gray-200 rounded-sm'></div></div></div>"
    },
    {
      "name": "Sidebar Left",
      "prompt": "Layout Configuration: Sidebar Left (narrow navigation sidebar on the left with main content area)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-2'><div class='w-6 bg-gray-300 rounded'></div><div class='flex-1 bg-gray-200 rounded'></div></div>"
    },
    {
      "name": "Sidebar Right", 
      "prompt": "Layout Configuration: Sidebar Right (main content with narrow sidebar on the right)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-2'><div class='flex-1 bg-gray-200 rounded'></div><div class='w-6 bg-gray-300 rounded'></div></div>"
    },
    {
      "name": "1-1 Split",
      "prompt": "Layout Configuration: 1-1 Split (two equal columns side by side)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-2'><div class='flex-1 bg-gray-250 rounded'></div><div class='flex-1 bg-gray-250 rounded'></div></div>"
    },
    {
      "name": "1-1 Vertical",
      "prompt": "Layout Configuration: 1-1 Vertical (two equal-height sections stacked vertically)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 space-y-2'><div class='h-8 bg-gray-250 rounded'></div><div class='h-8 bg-gray-250 rounded'></div></div>"
    },
    {
      "name": "1/3 2/3 Bento",
      "prompt": "Layout Configuration: 1/3 2/3 Bento (asymmetric grid with alternating 1/3-2/3 sections)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-2'><div class='w-6 bg-gray-250 rounded'></div><div class='flex-1 bg-gray-200 rounded'></div></div>"
    },
    {
      "name": "2/3 1/3 Bento", 
      "prompt": "Layout Configuration: 2/3 1/3 Bento (asymmetric grid with alternating 2/3-1/3 sections)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-2'><div class='flex-1 bg-gray-200 rounded'></div><div class='w-6 bg-gray-250 rounded'></div></div>"
    },
    {
      "name": "1×4 Bento",
      "prompt": "Layout Configuration: 1×4 Bento (full-width section on top with four equal columns below)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 space-y-1'><div class='h-8 bg-gray-250 rounded'></div><div class='grid grid-cols-4 gap-1 flex-1'><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div></div></div>"
    },
    {
      "name": "Feature Bento",
      "prompt": "Layout Configuration: Feature Bento (large featured cell with five smaller content areas)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='grid grid-cols-3 gap-1 h-full'><div class='col-span-2 row-span-2 bg-gray-250 rounded'></div><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div></div></div>"
    },
    {
      "name": "Featured Right",
      "prompt": "Layout Configuration: Featured Right (main content with two stacked sections on the right)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-2'><div class='flex-1 bg-gray-250 rounded'></div><div class='w-8 space-y-1'><div class='h-8 bg-gray-200 rounded'></div><div class='h-8 bg-gray-200 rounded'></div></div></div>"
    },
    {
      "name": "Featured Top",
      "prompt": "Layout Configuration: Featured Top (large featured section on top with columns below)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 space-y-1'><div class='h-12 bg-gray-250 rounded'></div><div class='grid grid-cols-3 gap-1 flex-1'><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div></div></div>"
    },
    {
      "name": "1/4 2/4 1/4 Bento",
      "prompt": "Layout Configuration: 1/4 2/4 1/4 Bento (asymmetric grid with 1/4-2/4-1/4 top row and equal bottom row)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='grid grid-cols-4 gap-1 h-full'><div class='bg-gray-250 rounded'></div><div class='col-span-2 bg-gray-200 rounded'></div><div class='bg-gray-250 rounded'></div></div></div>"
    },
    {
      "name": "2/4 1/4 1/4 Bento",
      "prompt": "Layout Configuration: 2/4 1/4 1/4 Bento (asymmetric grid with 2/4-1/4-1/4 top row and equal bottom row)", 
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='grid grid-cols-4 gap-1 h-full'><div class='col-span-2 bg-gray-250 rounded'></div><div class='bg-gray-200 rounded'></div><div class='bg-gray-200 rounded'></div></div></div>"
    },
    {
      "name": "2-1 Split",
      "prompt": "Layout Configuration: 2-1 Split (wider left column with narrower right column)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-2'><div class='flex-[2] bg-gray-250 rounded'></div><div class='flex-1 bg-gray-200 rounded'></div></div>"
    },
    {
      "name": "1-2 Split", 
      "prompt": "Layout Configuration: 1-2 Split (narrower left column with wider right column)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex gap-2'><div class='flex-1 bg-gray-200 rounded'></div><div class='flex-[2] bg-gray-250 rounded'></div></div>"
    },
    {
      "name": "1-1-1 Equal",
      "prompt": "Layout Configuration: 1-1-1 Equal (three equal columns in a row)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='grid grid-cols-3 gap-1 h-full'><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div></div></div>"
    },
    {
      "name": "Header Focus",
      "prompt": "Layout Configuration: Header Focus (prominent header with main content below)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 space-y-1'><div class='h-6 bg-gray-300 rounded'></div><div class='flex-1 bg-gray-200 rounded'></div></div>"
    },
    {
      "name": "3-3 Grid",
      "prompt": "Layout Configuration: 3-3 Grid (six equal cells arranged in a 3×2 grid)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='grid grid-cols-3 gap-1 h-full'><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div><div class='bg-gray-250 rounded'></div></div></div>"
    },
    {
      "name": "Carousel", 
      "prompt": "Layout Configuration: Carousel (horizontally scrolling content sections)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3 flex flex-col items-center justify-center space-y-2'><div class='flex gap-2'><div class='w-8 h-6 bg-gray-250 rounded'></div><div class='w-8 h-6 bg-gray-200 rounded'></div><div class='w-8 h-6 bg-gray-200 rounded'></div></div><div class='flex gap-1'><div class='w-1 h-1 bg-gray-400 rounded-full'></div><div class='w-1 h-1 bg-gray-300 rounded-full'></div><div class='w-1 h-1 bg-gray-300 rounded-full'></div></div></div>"
    },
    {
      "name": "Modal",
      "prompt": "Layout Configuration: Modal (focused overlay content on top of the main view)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded relative flex items-center justify-center'><div class='absolute inset-0 bg-gray-200/80 rounded'></div><div class='relative w-16 h-12 bg-white rounded border border-gray-300 shadow-sm'></div></div>"
    },
    {
      "name": "Alert",
      "prompt": "Layout Configuration: Alert (attention-grabbing notification element)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 flex items-center justify-center'><div class='w-3/4 h-6 bg-amber-100 border border-amber-200 rounded flex items-center px-2'><div class='w-1 h-1 bg-amber-500 rounded-full mr-1'></div><div class='h-0.5 bg-amber-400 rounded flex-1'></div></div></div>"
    }
  ]
  
  // ================================
  // FRAMING OPTIONS
  // ================================
  
  export const FRAMING_OPTIONS: FramingOption[] = [
    {
      "name": "Full Screen",
      "prompt": "Framing: Full Screen (full browser viewport width and height)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='w-full h-full bg-gray-200 rounded'></div></div>"
    },
    {
      "name": "Card", 
      "prompt": "Framing: Card (contained in a card with padding and shadow)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-3 flex items-center justify-center'><div class='w-3/4 h-3/4 bg-gray-300 rounded-lg shadow-sm border border-gray-400'><div class='w-full h-full bg-gray-150 rounded-md m-1'></div></div></div>"
    },
    {
      "name": "Browser",
      "prompt": "Framing: Browser (displayed in a browser window frame)", 
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='w-full h-full bg-gray-300 rounded border border-gray-400'><div class='h-3 bg-gray-200 rounded-t flex items-center px-1 gap-0.5'><div class='w-1 h-1 bg-red-400 rounded-full'></div><div class='w-1 h-1 bg-yellow-400 rounded-full'></div><div class='w-1 h-1 bg-green-400 rounded-full'></div><div class='ml-1 h-1 bg-gray-150 rounded flex-1'></div></div><div class='flex-1 bg-gray-150 rounded-b'></div></div></div>"
    },
    {
      "name": "Mac App",
      "prompt": "Framing: Mac App (styled as a native macOS application window)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2'><div class='w-full h-full bg-gray-300 rounded-lg border border-gray-400 shadow-sm'><div class='h-3 bg-gray-250 rounded-t-lg flex items-center px-1 gap-0.5'><div class='w-1.5 h-1.5 bg-red-500 rounded-full'></div><div class='w-1.5 h-1.5 bg-amber-400 rounded-full'></div><div class='w-1.5 h-1.5 bg-emerald-500 rounded-full'></div><div class='ml-1 w-4 h-1 bg-gray-200 rounded'></div></div><div class='flex-1 bg-gray-150 rounded-b-lg'></div></div></div>"
    },
    {
      "name": "Clay Web",
      "prompt": "Framing: Clay Web (displayed in a modern clay-style browser frame with rounded corners and subtle shadows)",
      "html": "<div class='w-full h-24 bg-gray-100 rounded p-2 flex items-center justify-center'><div class='w-4/5 h-4/5 bg-gradient-to-b from-gray-200 to-gray-300 rounded-xl shadow-lg border border-gray-400/50'><div class='w-full h-full bg-gray-100/80 rounded-lg m-0.5'></div></div></div>"
    }
  ]
  
  // ================================
  // STYLE OPTIONS
  // ================================
  
 // ================================
// STYLE OPTIONS  
// ================================

export const STYLE_OPTIONS: StyleOption[] = [
  {
    "name": "Flat",
    "prompt": "Apply a flat visual style",
    "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 space-y-2'><div class='h-2 bg-gray-200 rounded w-4/5'></div><div class='h-2 bg-gray-200 rounded w-3/4'></div><div class='h-2 bg-gray-200 rounded w-2/3'></div></div>"
  },
  {
    "name": "Outline", 
    "prompt": "Apply an outline visual style",
    "html": "<div class='w-full h-24 bg-gray-100 rounded p-4 space-y-2'><div class='h-2 border border-gray-300 rounded w-4/5'></div><div class='h-2 border border-gray-300 rounded w-3/4'></div><div class='h-2 border border-gray-300 rounded w-2/3'></div></div>"
  },
  {
    "name": "Minimalist",
    "prompt": "Apply a minimalist visual style", 
    "html": "<div class='w-full h-24 bg-gray-50 rounded p-4 space-y-3'><div class='h-1.5 bg-gray-150 rounded w-4/5'></div><div class='h-1.5 bg-gray-150 rounded w-3/4'></div><div class='h-1.5 bg-gray-150 rounded w-2/3'></div></div>"
  },
  {
    "name": "Glass",
    "prompt": "Apply a glass visual style",
    "html": "<div class='w-full h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded p-4 space-y-2 relative'><div class='absolute inset-0 bg-white/40 rounded'></div><div class='relative h-2 bg-white/70 rounded w-4/5'></div><div class='relative h-2 bg-white/60 rounded w-3/4'></div><div class='relative h-2 bg-white/50 rounded w-2/3'></div></div>"
  },
  {
    "name": "iOS",
    "prompt": "Apply an ios visual style",
    "html": "<div class='w-full h-24 bg-gray-100 rounded-3xl p-4 space-y-3 shadow-sm border border-gray-200'><div class='h-2 bg-gray-250 rounded-full w-4/5'></div><div class='h-2 bg-gray-250 rounded-full w-3/4'></div><div class='h-2 bg-gray-250 rounded-full w-2/3'></div></div>"
  },
  {
    "name": "Material",
    "prompt": "Apply a material visual style",
    "html": "<div class='w-full h-24 bg-gray-100 rounded-lg p-4 space-y-2 shadow-md border border-gray-200'><div class='h-3 bg-gray-300 rounded w-1/3 mb-1'></div><div class='h-2 bg-gray-200 rounded w-4/5'></div><div class='h-2 bg-gray-200 rounded w-3/4'></div></div>"
  }
]

// ================================
// THEME OPTIONS
// ================================

export const THEME_OPTIONS: ThemeOption[] = [
  {
    "name": "Light Mode",
    "prompt": "Use light mode colors",
    "html": "<div class='w-full h-24 bg-white rounded border border-gray-200 flex items-center justify-center'><div class='w-6 h-6 bg-yellow-400 rounded-full'></div></div>"
  },
  {
    "name": "Dark Mode", 
    "prompt": "Use dark mode colors",
    "html": "<div class='w-full h-24 bg-gray-900 rounded border border-gray-700 flex items-center justify-center'><div class='w-5 h-5 bg-white rounded-full'></div></div>"
  }
]

// ================================
// ACCENT COLORS
// ================================

export const ACCENT_COLORS: AccentColor[] = [
  { "name": "Primary", "prompt": "Accent Color: Primary (black)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-black'></div></div>" },
  { "name": "Blue", "prompt": "Accent Color: Blue (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-blue-500'></div></div>" },
  { "name": "Indigo", "prompt": "Accent Color: Indigo (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-indigo-500'></div></div>" },
  { "name": "Violet", "prompt": "Accent Color: Violet (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-violet-500'></div></div>" },
  { "name": "Purple", "prompt": "Accent Color: Purple (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-purple-500'></div></div>" },
  { "name": "Fuchsia", "prompt": "Accent Color: Fuchsia (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-fuchsia-500'></div></div>" },
  { "name": "Pink", "prompt": "Accent Color: Pink (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-pink-500'></div></div>" },
  { "name": "Rose", "prompt": "Accent Color: Rose (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-rose-500'></div></div>" },
  { "name": "Red", "prompt": "Accent Color: Red (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-red-500'></div></div>" },
  { "name": "Orange", "prompt": "Accent Color: Orange (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-orange-500'></div></div>" },
  { "name": "Amber", "prompt": "Accent Color: Amber (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-amber-500'></div></div>" },
  { "name": "Yellow", "prompt": "Accent Color: Yellow (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-yellow-500'></div></div>" },
  { "name": "Lime", "prompt": "Accent Color: Lime (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-lime-500'></div></div>" },
  { "name": "Green", "prompt": "Accent Color: Green (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-green-500'></div></div>" },
  { "name": "Emerald", "prompt": "Accent Color: Emerald (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-emerald-500'></div></div>" },
  { "name": "Teal", "prompt": "Accent Color: Teal (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-teal-500'></div></div>" },
  { "name": "Cyan", "prompt": "Accent Color: Cyan (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-cyan-500'></div></div>" },
  { "name": "Sky", "prompt": "Accent Color: Sky (Tailwind 500)", "html": "<div class='w-full h-24 bg-gray-100 rounded border border-gray-200 flex items-center justify-center'><div class='h-8 w-8 rounded-full bg-sky-500'></div></div>" }
]

// ================================
// BACKGROUND COLORS
// ================================

export const BACKGROUND_COLORS: BackgroundColor[] = [
  { "name": "Transparent", "prompt": "Background Color: Transparent (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-transparent relative'><div class='absolute inset-0 bg-[linear-gradient(45deg,#f3f4f6_25%,transparent_25%),linear-gradient(-45deg,#f3f4f6_25%,transparent_25%),linear-gradient(45deg,transparent_75%,#f3f4f6_75%),linear-gradient(-45deg,transparent_75%,#f3f4f6_75%)] bg-[length:8px_8px] bg-[0_0,0_4px,4px_-4px,-4px_0px] rounded'></div></div>" },
  { "name": "Neutral", "prompt": "Background Color: Neutral (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-neutral-100'></div>" },
  { "name": "Gray", "prompt": "Background Color: Gray (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-gray-100'></div>" },
  { "name": "Slate", "prompt": "Background Color: Slate (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-slate-100'></div>" },
  { "name": "Zinc", "prompt": "Background Color: Zinc (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-zinc-100'></div>" },
  { "name": "Stone", "prompt": "Background Color: Stone (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-stone-100'></div>" },
  { "name": "Rose", "prompt": "Background Color: Rose (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-rose-100'></div>" },
  { "name": "Red", "prompt": "Background Color: Red (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-red-100'></div>" },
  { "name": "Orange", "prompt": "Background Color: Orange (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-orange-100'></div>" },
  { "name": "Amber", "prompt": "Background Color: Amber (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-amber-100'></div>" },
  { "name": "Yellow", "prompt": "Background Color: Yellow (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-yellow-100'></div>" },
  { "name": "Lime", "prompt": "Background Color: Lime (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-lime-100'></div>" },
  { "name": "Green", "prompt": "Background Color: Green (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-green-100'></div>" },
  { "name": "Emerald", "prompt": "Background Color: Emerald (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-emerald-100'></div>" },
  { "name": "Teal", "prompt": "Background Color: Teal (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-teal-100'></div>" },
  { "name": "Cyan", "prompt": "Background Color: Cyan (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-cyan-100'></div>" },
  { "name": "Sky", "prompt": "Background Color: Sky (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-sky-100'></div>" },
  { "name": "Blue", "prompt": "Background Color: Blue (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-blue-100'></div>" },
  { "name": "Indigo", "prompt": "Background Color: Indigo (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-indigo-100'></div>" },
  { "name": "Violet", "prompt": "Background Color: Violet (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-violet-100'></div>" },
  { "name": "Purple", "prompt": "Background Color: Purple (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-purple-100'></div>" },
  { "name": "Fuchsia", "prompt": "Background Color: Fuchsia (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-fuchsia-100'></div>" },
  { "name": "Pink", "prompt": "Background Color: Pink (Tailwind 100)", "html": "<div class='w-full h-20 rounded border border-gray-200 bg-pink-100'></div>" }
]

// ================================
// BORDER COLORS
// ================================

export const BORDER_COLORS: BorderColor[] = [
  { "name": "Transparent", "prompt": "Border Color: Transparent (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-transparent bg-white'></div>" },
  { "name": "Neutral", "prompt": "Border Color: Neutral (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-neutral-200 bg-white'></div>" },
  { "name": "Gray", "prompt": "Border Color: Gray (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-gray-200 bg-white'></div>" },
  { "name": "Slate", "prompt": "Border Color: Slate (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-slate-200 bg-white'></div>" },
  { "name": "Zinc", "prompt": "Border Color: Zinc (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-zinc-200 bg-white'></div>" },
  { "name": "Stone", "prompt": "Border Color: Stone (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-stone-200 bg-white'></div>" },
  { "name": "Blue", "prompt": "Border Color: Blue (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-blue-200 bg-white'></div>" },
  { "name": "Indigo", "prompt": "Border Color: Indigo (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-indigo-200 bg-white'></div>" },
  { "name": "Violet", "prompt": "Border Color: Violet (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-violet-200 bg-white'></div>" },
  { "name": "Purple", "prompt": "Border Color: Purple (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-purple-200 bg-white'></div>" },
  { "name": "Fuchsia", "prompt": "Border Color: Fuchsia (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-fuchsia-200 bg-white'></div>" },
  { "name": "Pink", "prompt": "Border Color: Pink (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-pink-200 bg-white'></div>" },
  { "name": "Rose", "prompt": "Border Color: Rose (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-rose-200 bg-white'></div>" },
  { "name": "Red", "prompt": "Border Color: Red (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-red-200 bg-white'></div>" },
  { "name": "Orange", "prompt": "Border Color: Orange (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-orange-200 bg-white'></div>" },
  { "name": "Amber", "prompt": "Border Color: Amber (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-amber-200 bg-white'></div>" },
  { "name": "Yellow", "prompt": "Border Color: Yellow (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-yellow-200 bg-white'></div>" },
  { "name": "Lime", "prompt": "Border Color: Lime (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-lime-200 bg-white'></div>" },
  { "name": "Green", "prompt": "Border Color: Green (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-green-200 bg-white'></div>" },
  { "name": "Emerald", "prompt": "Border Color: Emerald (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-emerald-200 bg-white'></div>" },
  { "name": "Teal", "prompt": "Border Color: Teal (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-teal-200 bg-white'></div>" },
  { "name": "Cyan", "prompt": "Border Color: Cyan (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-cyan-200 bg-white'></div>" },
  { "name": "Sky", "prompt": "Border Color: Sky (Tailwind 200)", "html": "<div class='w-full h-20 rounded-lg border-2 border-sky-200 bg-white'></div>" }
]

// ================================
// SHADOWS
// ================================

export const SHADOWS: Shadow[] = [
  { "name": "None", "prompt": "none: no prompt", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-none'></div>" },
  { "name": "Small", "prompt": "Shadow: Small (shadow-sm)", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-sm'></div>" },
  { "name": "Medium", "prompt": "Shadow: Medium (shadow-md)", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-md'></div>" },
  { "name": "Large", "prompt": "Shadow: Large (shadow-lg)", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-lg'></div>" },
  { "name": "Extra Large", "prompt": "Shadow: Extra Large (shadow-xl)", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-xl'></div>" },
  { "name": "XXL", "prompt": "Shadow: XXL (shadow-2xl)", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-2xl'></div>" },
  { "name": "Beautiful sm", "prompt": "Shadow: Beautiful sm", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-[0px_2px_3px_-1px_rgba(0,0,0,0.1),0px_1px_0px_0px_rgba(25,28,33,0.02),0px_0px_0px_1px_rgba(25,28,33,0.08)]'></div>" },
  { "name": "Beautiful md", "prompt": "Shadow: Beautiful md", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-[0px_0px_0px_1px_rgba(0,0,0,0.06),0px_1px_1px_-0.5px_rgba(0,0,0,0.06),0px_3px_3px_-1.5px_rgba(0,0,0,0.06),0px_6px_6px_-3px_rgba(0,0,0,0.06),0px_12px_12px_-6px_rgba(0,0,0,0.06),0px_24px_24px_-12px_rgba(0,0,0,0.06)]'></div>" },
  { "name": "Beautiful lg", "prompt": "Shadow: Beautiful lg", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-[0_2.8px_2.2px_rgba(0,0,0,0.034),0_6.7px_5.3px_rgba(0,0,0,0.048),0_12.5px_10px_rgba(0,0,0,0.06),0_22.3px_17.9px_rgba(0,0,0,0.072),0_41.8px_33.4px_rgba(0,0,0,0.086),0_100px_80px_rgba(0,0,0,0.12)]'></div>" },
  { "name": "Light Blue sm", "prompt": "Shadow: Light Blue sm", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-[rgba(14,63,126,0.04)_0px_0px_0px_1px,rgba(42,51,69,0.04)_0px_1px_1px_-0.5px,rgba(42,51,70,0.04)_0px_3px_3px_-1.5px,rgba(42,51,70,0.04)_0px_6px_6px_-3px,rgba(14,63,126,0.04)_0px_12px_12px_-6px,rgba(14,63,126,0.04)_0px_24px_24px_-12px]'></div>" },
  { "name": "Light Blue md", "prompt": "Shadow: Light Blue md", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-[rgba(50,50,93,0.25)_0px_13px_27px_-5px,rgba(0,0,0,0.3)_0px_8px_16px_-8px]'></div>" },
  { "name": "Light Blue lg", "prompt": "Shadow: Light Blue lg", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-[rgba(255,255,255,0.1)_0px_1px_1px_0px_inset,rgba(50,50,93,0.25)_0px_50px_100px_-20px,rgba(0,0,0,0.3)_0px_30px_60px_-30px]'></div>" },
  { "name": "Bevel", "prompt": "Shadow: Bevel", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-[rgba(50,50,93,0.25)_0px_50px_100px_-20px,rgba(0,0,0,0.3)_0px_30px_60px_-30px,rgba(10,37,64,0.35)_0px_-2px_6px_0px_inset]'></div>" },
  { "name": "3D", "prompt": "Shadow: 3D", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-[rgba(0,0,0,0.17)_0px_-23px_25px_0px_inset,rgba(0,0,0,0.15)_0px_-36px_30px_0px_inset,rgba(0,0,0,0.1)_0px_-79px_40px_0px_inset,rgba(0,0,0,0.06)_0px_2px_1px,rgba(0,0,0,0.09)_0px_4px_2px,rgba(0,0,0,0.09)_0px_8px_4px,rgba(0,0,0,0.09)_0px_16px_8px,rgba(0,0,0,0.09)_0px_32px_16px]'></div>" },
  { "name": "Inner Shadow", "prompt": "Shadow: Inner Shadow", "html": "<div class='w-full h-20 rounded-lg border border-gray-200 bg-white shadow-[rgba(50,50,93,0.25)_0px_30px_60px_-12px_inset,rgba(0,0,0,0.3)_0px_18px_36px_-18px_inset]'></div>" }
]
  // ================================
  // TYPOGRAPHY OPTIONS
  // ================================
  
  export const TYPEFACE_FAMILIES: TypefaceOption[] = [
    {
      "name": "Sans",
      "prompt": "Use sans fonts",
      "html": "<div class='w-[120px] h-[80px] grid place-items-center rounded-2xl border bg-white font-sans text-gray-800 text-lg'>Type</div>"
    },
    {
      "name": "Serif",
      "prompt": "Use serif fonts",
      "html": "<div class='w-[120px] h-[80px] grid place-items-center rounded-2xl border bg-white font-serif text-gray-800 text-lg'>Type</div>"
    },
    {
      "name": "Monospace",
      "prompt": "Use monospace fonts",
      "html": "<div class='w-[120px] h-[80px] grid place-items-center rounded-2xl border bg-white font-mono text-gray-800 text-lg'>Type</div>"
    },
    {
      "name": "Condensed",
      "prompt": "Use condensed fonts",
      "html": "<div class='w-[120px] h-[80px] grid place-items-center rounded-2xl border bg-white font-sans tracking-tight text-gray-800 text-lg'>Type</div>"
    },
    {
      "name": "Expanded",
      "prompt": "Use expanded fonts",
      "html": "<div class='w-[120px] h-[80px] grid place-items-center rounded-2xl border bg-white font-sans tracking-wider text-gray-800 text-lg'>Type</div>"
    },
    {
      "name": "Rounded",
      "prompt": "Use rounded fonts",
      "html": "<div class='w-[120px] h-[80px] grid place-items-center rounded-2xl border bg-white font-sans text-gray-800 text-lg rounded-lg'>Type</div>"
    },
    {
      "name": "Handwritten",
      "prompt": "Use handwritten fonts",
      "html": "<div class='w-[120px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[cursive] text-gray-800 text-lg italic'>Type</div>"
    }
  ]

  export const HEADING_FONT: HeadingFont[] = [
    {
      "name": "Inter",
      "prompt": "Use Inter for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Inter] text-xl'>Title</div>"
    },
    {
      "name": "Geist",
      "prompt": "Use Geist for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Geist] text-xl'>Title</div>"
    },
    {
      "name": "Manrope",
      "prompt": "Use Manrope for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Manrope] text-xl'>Title</div>"
    },
    {
      "name": "Playfair Display",
      "prompt": "Use Playfair Display for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Playfair_Display] text-xl'>Title</div>"
    },
    {
      "name": "Instrument Serif",
      "prompt": "Use Instrument Serif for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Instrument_Serif] text-xl'>Title</div>"
    },
    {
      "name": "Plex Serif",
      "prompt": "Use Plex Serif for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[IBM_Plex_Serif] text-xl'>Title</div>"
    },
    {
      "name": "Nunito",
      "prompt": "Use Nunito for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Nunito] text-xl'>Title</div>"
    },
    {
      "name": "Varela Round",
      "prompt": "Use Varela Round for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Varela_Round] text-xl'>Title</div>"
    },
    {
      "name": "Geist Mono",
      "prompt": "Use Geist Mono for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Geist_Mono] text-xl'>Title</div>"
    },
    {
      "name": "Space Mono",
      "prompt": "Use Space Mono for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Space_Mono] text-xl'>Title</div>"
    },
    {
      "name": "Source Code",
      "prompt": "Use Source Code for headings",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Source_Code_Pro] text-xl'>Title</div>"
    }
  ]

  export const BODY_FONT: BodyFont[] =  [
    {
      "name": "Inter",
      "prompt": "Use Inter for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Inter] text-base'>Body</div>"
    },
    {
      "name": "Geist",
      "prompt": "Use Geist for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Geist] text-base'>Body</div>"
    },
    {
      "name": "Manrope",
      "prompt": "Use Manrope for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Manrope] text-base'>Body</div>"
    },
    {
      "name": "Playfair Display",
      "prompt": "Use Playfair Display for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Playfair_Display] text-base'>Body</div>"
    },
    {
      "name": "Instrument Serif",
      "prompt": "Use Instrument Serif for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Instrument_Serif] text-base'>Body</div>"
    },
    {
      "name": "Plex Serif",
      "prompt": "Use Plex Serif for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[IBM_Plex_Serif] text-base'>Body</div>"
    },
    {
      "name": "Nunito",
      "prompt": "Use Nunito for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Nunito] text-base'>Body</div>"
    },
    {
      "name": "Varela Round",
      "prompt": "Use Varela Round for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Varela_Round] text-base'>Body</div>"
    },
    {
      "name": "Geist Mono",
      "prompt": "Use Geist Mono for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Geist_Mono] text-base'>Body</div>"
    },
    {
      "name": "Space Mono",
      "prompt": "Use Space Mono for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Space_Mono] text-base'>Body</div>"
    },
    {
      "name": "Source Code",
      "prompt": "Use Source Code for body text",
      "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white font-[Source_Code_Pro] text-base'>Body</div>"
    }
  ]

  export const HEADING_SIZE: HeadingSize[] = [
    { "name": "20–32px", "prompt": "Use heading size 20-32px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[20px] md:text-[32px] font-bold'>Title</div>" },
    { "name": "32–40px", "prompt": "Use heading size 32-40px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[32px] md:text-[40px] font-bold'>Title</div>" },
    { "name": "48–64px", "prompt": "Use heading size 48-64px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[48px] md:text-[64px] font-bold'>Title</div>" },
    { "name": "64–80px", "prompt": "Use heading size 64-80px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[64px] md:text-[80px] font-bold'>Title</div>" }
  ]  
  
  export const SUBHEADING_SIZE: SubHeadingSize[] = [
    { "name": "16–20px", "prompt": "Use subheading size 16-20px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[16px] md:text-[20px] font-semibold'>Subtitle</div>" },
    { "name": "20–24px", "prompt": "Use subheading size 20-24px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[20px] md:text-[24px] font-semibold'>Subtitle</div>" },
    { "name": "24–28px", "prompt": "Use subheading size 24-28px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[24px] md:text-[28px] font-semibold'>Subtitle</div>" },
    { "name": "28–32px", "prompt": "Use subheading size 28-32px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[28px] md:text-[32px] font-semibold'>Subtitle</div>" }
  ]

  export const BODY_TEXT_SIZE: BodyTextSize[] = [
    { "name": "16–20px", "prompt": "Use body text size 16-20px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[16px] md:text-[20px] font-semibold'>Body</div>" },
    { "name": "20–24px", "prompt": "Use body text size 20-24px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[20px] md:text-[24px] font-semibold'>Body</div>" },
    { "name": "24–28px", "prompt": "Use body text size 24-28px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[24px] md:text-[28px] font-semibold'>Body</div>" },
    { "name": "28–32px", "prompt": "Use body text size 28-32px", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-[28px] md:text-[32px] font-semibold'>Body</div>" }
  ]

  export const HEADING_FONT_WEIGHT: HeadingFontWeight[] = [
    { "name": "Light", "prompt": "Apply light font weight to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl font-light'>Title</div>" },
    { "name": "Regular", "prompt": "Apply regular font weight to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl font-normal'>Title</div>" },
    { "name": "Medium", "prompt": "Apply medium font weight to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl font-medium'>Title</div>" },
    { "name": "Semibold", "prompt": "Apply semibold font weight to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl font-semibold'>Title</div>" },
    { "name": "Bold", "prompt": "Apply bold font weight to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl font-bold'>Title</div>" },
    { "name": "Black", "prompt": "Apply black font weight to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl font-black'>Title</div>" }
  ]

  export const HEADING_LETTER_SPACING: LetterSpacing[] = [
    { "name": "Tighter", "prompt": "Apply tighter letter spacing to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl tracking-tighter'>Title</div>" },
    { "name": "Tight", "prompt": "Apply tight letter spacing to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl tracking-tight'>Title</div>" },
    { "name": "Normal", "prompt": "Apply normal letter spacing to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl tracking-normal'>Title</div>" },
    { "name": "Wide", "prompt": "Apply wide letter spacing to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl tracking-wide'>Title</div>" },
    { "name": "Wider", "prompt": "Apply wider letter spacing to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl tracking-wider'>Title</div>" },
    { "name": "Widest", "prompt": "Apply widest letter spacing to headings", "html": "<div class='w-[140px] h-[80px] grid place-items-center rounded-2xl border bg-white text-xl tracking-widest'>Title</div>" }
  ]
  
  // ================================
  // ANIMATION OPTIONS
  // ================================
  
  export const ANIMATION_TYPES: AnimationType[] = [
    { "name": "Fade", "prompt": "Apply fade animation", "html": "<div class='animate-fade w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Slide", "prompt": "Apply slide animation", "html": "<div class='animate-slide w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Scale", "prompt": "Apply scale animation", "html": "<div class='animate-scale w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Rotate", "prompt": "Apply rotate animation", "html": "<div class='animate-rotate w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Blur", "prompt": "Apply blur animation", "html": "<div class='animate-blur w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "3D", "prompt": "Apply 3D animation", "html": "<div class='animate-3d w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Pulse", "prompt": "Apply pulse animation", "html": "<div class='animate-pulse w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Shake", "prompt": "Apply shake animation", "html": "<div class='animate-shake w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Bounce", "prompt": "Apply bounce animation", "html": "<div class='animate-bounce w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Morph", "prompt": "Apply morph animation", "html": "<div class='animate-morph w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Skew", "prompt": "Apply skew animation", "html": "<div class='animate-skew w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Color", "prompt": "Apply color animation", "html": "<div class='animate-color w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Hue", "prompt": "Apply hue animation", "html": "<div class='animate-hue w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Perspective", "prompt": "Apply perspective animation", "html": "<div class='animate-perspective w-[100px] h-[100px] bg-gray-400'></div>" },
    { "name": "Clip", "prompt": "Apply clip animation", "html": "<div class='animate-clip w-[100px] h-[100px] bg-gray-400'></div>" }
  ]
  
  export const ANIMATION_SCENES: AnimationScene[] = [
    {
      "name": "All at once",
      "prompt": "Animate all at once",
      "html": "<div class='w-[140px] h-[80px] rounded-2xl border bg-white grid grid-cols-3 gap-2 p-3'><div class='bg-gray-300 rounded'></div><div class='bg-gray-300 rounded'></div><div class='bg-gray-300 rounded'></div><div class='bg-gray-300 rounded'></div><div class='bg-gray-300 rounded'></div><div class='bg-gray-300 rounded'></div><div class='bg-gray-300 rounded'></div><div class='bg-gray-300 rounded'></div><div class='bg-gray-300 rounded'></div></div>"
    },
    {
      "name": "Sequence",
      "prompt": "Animate sequence",
      "html": "<div class='w-[140px] h-[80px] rounded-2xl border bg-white flex items-center justify-between p-4'><div class='h-6 w-6 rounded bg-gray-300'></div><div class='h-6 w-6 rounded bg-gray-300 opacity-80'></div><div class='h-6 w-6 rounded bg-gray-300 opacity-60'></div><div class='h-6 w-6 rounded bg-gray-300 opacity-40'></div></div>"
    },
    {
      "name": "Word by word",
      "prompt": "Animate word by word",
      "html": "<div class='w-[140px] h-[80px] rounded-2xl border bg-white flex items-center justify-center gap-2 px-3'><span class='px-2 py-1 rounded bg-gray-200'>Word</span><span class='px-2 py-1 rounded bg-gray-100'>Word</span><span class='px-2 py-1 rounded bg-gray-100'>Word</span></div>"
    },
    {
      "name": "Letter by letter",
      "prompt": "Animate letter by letter",
      "html": "<div class='w-[140px] h-[80px] rounded-2xl border bg-white flex items-center justify-center gap-1 text-lg font-semibold text-gray-700'><span class='px-1 rounded bg-gray-200'>T</span><span class='px-1 rounded bg-gray-100'>I</span><span class='px-1 rounded bg-gray-100'>T</span><span class='px-1 rounded bg-gray-100'>L</span><span class='px-1 rounded bg-gray-100'>E</span></div>"
    }
  ]

  export const ANIMATION_TIMING: AnimationType[] = [
    {
      "name": "Linear",
      "prompt": "Use linear easing",
      "html": "<div class='w-[160px] h-[84px] rounded-2xl border bg-white grid place-items-center p-3'><svg viewBox='0 0 100 40' class='w-full h-10'><path d='M5 35 L95 5' fill='none' stroke='currentColor' class='text-gray-500' stroke-width='3' stroke-linecap='round'/></svg><div class='text-xs text-gray-500 -mt-1'>Linear</div></div>"
    },
    {
      "name": "Ease",
      "prompt": "Use ease easing",
      "html": "<div class='w-[160px] h-[84px] rounded-2xl border bg-white grid place-items-center p-3'><svg viewBox='0 0 100 40' class='w-full h-10'><path d='M5 35 C25 5, 75 5, 95 35' fill='none' stroke='currentColor' class='text-gray-500' stroke-width='3' stroke-linecap='round'/></svg><div class='text-xs text-gray-500 -mt-1'>Ease</div></div>"
    },
    {
      "name": "Ease In",
      "prompt": "Use ease in easing",
      "html": "<div class='w-[160px] h-[84px] rounded-2xl border bg-white grid place-items-center p-3'><svg viewBox='0 0 100 40' class='w-full h-10'><path d='M5 35 C10 35, 30 35, 95 5' fill='none' stroke='currentColor' class='text-gray-500' stroke-width='3' stroke-linecap='round'/></svg><div class='text-xs text-gray-500 -mt-1'>Ease In</div></div>"
    },
    {
      "name": "Ease Out",
      "prompt": "Use ease out easing",
      "html": "<div class='w-[160px] h-[84px] rounded-2xl border bg-white grid place-items-center p-3'><svg viewBox='0 0 100 40' class='w-full h-10'><path d='M5 35 C70 5, 90 5, 95 5' fill='none' stroke='currentColor' class='text-gray-500' stroke-width='3' stroke-linecap='round'/></svg><div class='text-xs text-gray-500 -mt-1'>Ease Out</div></div>"
    },
    {
      "name": "Ease In Out",
      "prompt": "Use ease in out easing",
      "html": "<div class='w-[160px] h-[84px] rounded-2xl border bg-white grid place-items-center p-3'><svg viewBox='0 0 100 40' class='w-full h-10'><path d='M5 35 C25 35, 35 5, 50 5 S75 35, 95 35' fill='none' stroke='currentColor' class='text-gray-500' stroke-width='3' stroke-linecap='round'/></svg><div class='text-xs text-gray-500 -mt-1'>Ease In Out</div></div>"
    },
    {
      "name": "Spring",
      "prompt": "Use spring easing",
      "html": "<div class='w-[160px] h-[84px] rounded-2xl border bg-white grid place-items-center p-3'><svg viewBox='0 0 100 40' class='w-full h-10'><path d='M5 30 Q15 10 25 30 T45 30 T65 30 T85 30' fill='none' stroke='currentColor' class='text-gray-500' stroke-width='3' stroke-linecap='round'/></svg><div class='text-xs text-gray-500 -mt-1'>Spring</div></div>"
    },
    {
      "name": "Bounce",
      "prompt": "Use bounce easing",
      "html": "<div class='w-[160px] h-[84px] rounded-2xl border bg-white grid place-items-center p-3'><svg viewBox='0 0 100 40' class='w-full h-10'><path d='M5 30 L30 5 L55 28 L75 10 L95 30' fill='none' stroke='currentColor' class='text-gray-500' stroke-width='3' stroke-linecap='round'/></svg><div class='text-xs text-gray-500 -mt-1'>Bounce</div></div>"
    }
  ]

  export const ANIMATION_ITERATIONS: AnimationType[] = [
    {
      "name": "Once",
      "prompt": "Repeat animation once",
      "html": "<div class='w-[120px] h-[80px] rounded-2xl border bg-white grid place-items-center'><div class='text-lg font-semibold'>1×</div><div class='text-xs text-gray-500 -mt-1'>Once</div></div>"
    },
    {
      "name": "Twice",
      "prompt": "Repeat animation twice",
      "html": "<div class='w-[120px] h-[80px] rounded-2xl border bg-white grid place-items-center'><div class='text-lg font-semibold'>2×</div><div class='text-xs text-gray-500 -mt-1'>Twice</div></div>"
    },
    {
      "name": "Thrice",
      "prompt": "Repeat animation thrice",
      "html": "<div class='w-[120px] h-[80px] rounded-2xl border bg-white grid place-items-center'><div class='text-lg font-semibold'>3×</div><div class='text-xs text-gray-500 -mt-1'>Thrice</div></div>"
    },
    {
      "name": "Infinite",
      "prompt": "Repeat animation infinite",
      "html": "<div class='w-[120px] h-[80px] rounded-2xl border bg-white grid place-items-center'><div class='text-lg font-semibold'>∞</div><div class='text-xs text-gray-500 -mt-1'>Infinite</div></div>"
    }
  ]

  export const ANIMATION_DIRECTION: AnimationType[] = [
    {
      "name": "Normal",
      "prompt": "Animation direction: normal",
      "html": "<div class='w-[120px] h-[80px] rounded-2xl border bg-white grid place-items-center'><svg viewBox='0 0 64 24' class='w-14 h-6'><path d='M4 12 H52' stroke='currentColor' class='text-gray-500' stroke-width='3'/><path d='M44 4 L60 12 L44 20 Z' fill='currentColor' class='text-gray-500'/></svg></div>"
    },
    {
      "name": "Reverse",
      "prompt": "Animation direction: reverse",
      "html": "<div class='w-[120px] h-[80px] rounded-2xl border bg-white grid place-items-center'><svg viewBox='0 0 64 24' class='w-14 h-6'><path d='M12 12 H60' stroke='currentColor' class='text-gray-500' stroke-width='3'/><path d='M4 12 L20 4 V20 Z' fill='currentColor' class='text-gray-500'/></svg></div>"
    },
    {
      "name": "Alternate",
      "prompt": "Animation direction: alternate",
      "html": "<div class='w-[120px] h-[80px] rounded-2xl border bg-white grid place-items-center'><svg viewBox='0 0 80 24' class='w-20 h-6'><path d='M4 12 H36' stroke='currentColor' class='text-gray-500' stroke-width='3'/><path d='M28 4 L44 12 L28 20 Z' fill='currentColor' class='text-gray-500'/><path d='M44 12 H76' stroke='currentColor' class='text-gray-500' stroke-width='3'/></svg></div>"
    },
    {
      "name": "Alternate Reverse",
      "prompt": "Animation direction: alternate reverse",
      "html": "<div class='w-[120px] h-[80px] rounded-2xl border bg-white grid place-items-center'><svg viewBox='0 0 80 24' class='w-20 h-6'><path d='M4 12 H36' stroke='currentColor' class='text-gray-500' stroke-width='3'/><path d='M36 12 L20 4 V20 Z' fill='currentColor' class='text-gray-500'/><path d='M44 12 H76' stroke='currentColor' class='text-gray-500' stroke-width='3'/></svg></div>"
    }
  ]

