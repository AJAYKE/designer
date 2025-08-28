// ================================
// CORE PROMPT BUILDER TYPES
// ================================

export type Platform = 'web' | 'mobile'

export interface LayoutType {
  name: string
  prompt: string
  html: string
}

export interface LayoutConfiguration {
  name: string
  prompt: string
  html: string
}

export interface FramingOption {
  name: string
  prompt: string
  html: string
}

export interface StyleOption {
  name: string
  prompt: string
  html: string
}

export interface ThemeOption {
  name: string
  prompt: string
  html: string
}

export interface AccentColor {
  name: string
  prompt: string
  html: string
}

export interface BackgroundColor {
  name: string
  prompt: string
  html: string
}

export interface BorderColor {
  name: string
  prompt: string
  html: string
}

export interface Shadow {
  name: string
  prompt: string
  html: string
}

export interface TypefaceOption {
  name: string
  prompt: string
  html: string
}

export interface HeadingFont {
  name: string
  prompt: string
  html: string
}

export interface BodyFont {
  name: string
  prompt: string
  html: string
}

export interface HeadingSize {
  name: string
  prompt: string
  html: string
}

export interface SubHeadingSize {
  name: string
  prompt: string
  html: string
}

export interface BodyTextSize {
  name: string
  prompt: string
  html: string
}

export interface HeadingFontWeight {
  name: string
  prompt: string
  html: string
}

export interface SubHeadingFontWeight {
  name: string
  prompt: string
  html: string
}

export interface BodyFontWeight {
  name: string
  prompt: string
  html: string
}

export interface FontSize {
  name: string
  prompt: string
  html: string
}

export interface FontWeight {
  name: string
  prompt: string
  html: string
}

export interface LetterSpacing {
  name: string
  prompt: string
  html: string
}

export interface AnimationType {
  name: string
  prompt: string
  html: string
}

export interface AnimationScene {
  name: string
  prompt: string
  html: string
}

export interface AnimationTiming {
  name: string
  prompt: string
  html: string
}

export interface AnimationIteration {
  name: string
  prompt: string
  html: string
}

export interface AnimationDirection {
  name: string
  prompt: string
  html: string
}

// ================================
// PROMPT BUILDER STATE
// ================================

export interface PromptBuilderState {
  platform: Platform
  layoutType: LayoutType | null
  layoutConfiguration: LayoutConfiguration | null
  framing: FramingOption | null
  style: StyleOption | null
  theme: ThemeOption | null
  accentColor: AccentColor | null
  backgroundColor: BackgroundColor | null
  borderColor: BorderColor | null
  shadow: Shadow | null
  typefaceFamily: TypefaceOption | null
  headingFont: TypefaceOption | null
  bodyFont: TypefaceOption | null
  headingSize: FontSize | null
  subheadingSize: FontSize | null
  bodyTextSize: FontSize | null
  headingFontWeight: FontWeight | null
  headingLetterSpacing: LetterSpacing | null
  animationType: AnimationType[]
  animationScene: AnimationScene | null
  animationDuration: number
  animationDelay: number
  animationTiming: AnimationTiming | null
  animationIterations: AnimationIteration | null
  animationDirection: AnimationDirection | null
}

// ================================
// GENERATED PROMPTS
// ================================

export interface GeneratedPrompt {
  id: string
  text: string
  category: string
  removable: boolean
}

// ================================
// DESIGN GENERATION
// ================================

export interface GenerationState {
  status: 'idle' | 'planning' | 'generating' | 'enhancing' | 'complete' | 'error'
  plan: string | null
  code: string | null
  html: string | null
  css: string | null
  javascript: string | null
  images: UnsplashImage[]
  progress: number
  error?: string
}

export interface UnsplashImage {
  id: string
  url: string
  alt: string
  width: number
  height: number
  author: string
}

// ================================
// API TYPES
// ================================

export interface PromptConfig {
  platform: Platform
  layoutType?: string
  layoutConfiguration?: string
  framing?: string
  style?: string
  theme?: string
  accentColor?: string
  backgroundColor?: string
  borderColor?: string
  shadow?: string
  typefaceFamily?: string
  headingFont?: string
  bodyFont?: string
  headingSize?: string
  subheadingSize?: string
  bodyTextSize?: string
  headingFontWeight?: string
  headingLetterSpacing?: string
  animationType?: string[]
  animationScene?: string
  animationDuration?: number
  animationDelay?: number
  animationTiming?: string
  animationIterations?: string
  animationDirection?: string
  customPrompts?: string[]
}

// ================================
// UI COMPONENT TYPES
// ================================

export interface OptionCardProps {
  option: LayoutType | StyleOption | ThemeOption | any
  isSelected: boolean
  onClick: () => void
  className?: string
}

export interface PreviewFrameProps {
  html: string
  css?: string
  javascript?: string
  className?: string
}

export interface DeviceFrame {
  name: string
  width: number
  height: number
  className: string
}

// ================================
// RESPONSIVE TYPES
// ================================

export type Breakpoint = 'sm' | 'md' | 'lg' | 'xl' | '2xl'

export interface ResponsiveState {
  screenSize: Breakpoint
  isMobile: boolean
  isTablet: boolean
  isDesktop: boolean
}

// ================================
// THEME TYPES
// ================================

export type ThemeMode = 'light' | 'dark' | 'system'

export interface ThemeColors {
  primary: string
  background: string
  foreground: string
  muted: string
  border: string
  accent: string
}

export interface ThemeConfig {
  light: ThemeColors
  dark: ThemeColors
}

// ================================
// UTILITY TYPES
// ================================

export type Optional<T, K extends keyof T> = Pick<Partial<T>, K> & Omit<T, K>

export type DeepPartial<T> = {
  [P in keyof T]?: DeepPartial<T[P]>
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

export interface StreamChunk {
  type: 'progress' | 'plan' | 'code' | 'images' | 'complete' | 'error'
  data: any
  progress?: number
}