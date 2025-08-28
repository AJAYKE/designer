import {
  ACCENT_COLORS,
  ANIMATION_TYPES,
  BACKGROUND_COLORS,
  BODY_FONT,
  BODY_TEXT_SIZE,
  BORDER_COLORS,
  FRAMING_OPTIONS,
  HEADING_FONT,
  HEADING_FONT_WEIGHT,
  HEADING_LETTER_SPACING,
  HEADING_SIZE,
  LAYOUT_CONFIGURATIONS,
  SHADOWS,
  STYLE_OPTIONS,
  SUBHEADING_SIZE,
  THEME_OPTIONS,
  TYPEFACE_FAMILIES,
  WEB_LAYOUT_TYPES
} from '@/lib/prompt-builder-config'
import { AnimationDirection, AnimationIteration, AnimationTiming, GeneratedPrompt, Platform, PromptBuilderState } from '@/lib/types'
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface PromptBuilderStore extends PromptBuilderState {
  // Actions
  setPlatform: (platform: Platform) => void
  setLayoutType: (layoutType: string) => void
  setLayoutConfiguration: (config: string) => void
  setFraming: (framing: string) => void
  setStyle: (style: string) => void
  setTheme: (theme: string) => void
  setAccentColor: (color: string) => void
  setBackgroundColor: (color: string) => void
  setBorderColor: (color: string) => void
  setShadow: (shadow: string) => void
  setTypefaceFamily: (family: string) => void
  setHeadingFont: (font: string) => void
  setBodyFont: (font: string) => void
  setHeadingSize: (size: string) => void
  setSubheadingSize: (size: string) => void
  setBodyTextSize: (size: string) => void
  setHeadingFontWeight: (weight: string) => void
  setHeadingLetterSpacing: (spacing: string) => void
  addAnimationType: (animationType: string) => void
  removeAnimationType: (animationType: string) => void
  setAnimationDuration: (duration: number) => void
  setAnimationDelay: (delay: number) => void
  setAnimationTiming: (timing: AnimationTiming) => void
  setAnimationIterations: (iterations: AnimationIteration) => void
  setAnimationDirection: (direction: AnimationDirection) => void
  
  // Generated prompts
  generatedPrompts: GeneratedPrompt[]
  addGeneratedPrompt: (prompt: Omit<GeneratedPrompt, 'id'>) => void
  removeGeneratedPrompt: (id: string) => void
  updateGeneratedPrompt: (id: string, text: string) => void
  
  // Utility actions
  reset: () => void
  exportConfig: () => string
  importConfig: (config: string) => void
  generateFinalPrompt: () => string
}

const initialState: PromptBuilderState = {
  platform: 'web',
  layoutType: null,
  layoutConfiguration: null,
  framing: null,
  style: null,
  theme: null,
  accentColor: null,
  backgroundColor: null,
  borderColor: null,
  shadow: null,
  typefaceFamily: null,
  headingFont: null,
  bodyFont: null,
  headingSize: null,
  subheadingSize: null,
  bodyTextSize: null,
  headingFontWeight: null,
  headingLetterSpacing: null,
  animationType: [],
  animationScene: null,
  animationDuration: 1.8,
  animationDelay: 0,
  animationTiming: null,
  animationIterations: null,
  animationDirection: null,
}

export const usePromptBuilderStore = create<PromptBuilderStore>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,
        generatedPrompts: [],

        // Platform
        setPlatform: (platform) => {
          set({ platform })
          // Reset selections when switching platforms
          set({ 
            layoutType: null,
            layoutConfiguration: null,
            style: null
          })
        },

        // Layout Type
        setLayoutType: (layoutTypeName) => {
          const layoutType = WEB_LAYOUT_TYPES.find(lt => lt.name === layoutTypeName)
          set({ layoutType })
          
          // Auto-generate prompt when layout is selected
          if (layoutType) {
            get().addGeneratedPrompt({
              text: layoutType.prompt,
              category: 'Layout',
              removable: true
            })
          }
        },

        // Layout Configuration
        setLayoutConfiguration: (configName) => {
          const config = LAYOUT_CONFIGURATIONS.find(lc => lc.name === configName)
          set({ layoutConfiguration: config })
          
          if (config) {
            get().addGeneratedPrompt({
              text: config.prompt,
              category: 'Configuration',
              removable: true
            })
          }
        },

        // Framing
        setFraming: (framingName: string) => {
          const framing = FRAMING_OPTIONS.find(f => f.name === framingName)
          set({ framing })
          
          if (framing) {
            get().addGeneratedPrompt({
              text: framing.prompt,
              category: 'Framing',
              removable: true
            })
          }
        },

        // Style
        setStyle: (styleName) => {
          const style = STYLE_OPTIONS.find(s => s.name === styleName)
          set({ style })
          
          if (style) {
            get().addGeneratedPrompt({
              text: style.prompt,
              category: 'Style',
              removable: true
            })
          }
        },

        // Theme
        setTheme: (themeName) => {
          const theme = THEME_OPTIONS.find(t => t.name === themeName)
          set({ theme })
          
          if (theme) {
            get().addGeneratedPrompt({
              text: theme.prompt,
              category: 'Theme',
              removable: true
            })
          }
        },

        // Accent Color
        setAccentColor: (colorName) => {
          const accentColor = ACCENT_COLORS.find(c => c.name === colorName)
          set({ accentColor })
          
          if (accentColor) {
            get().addGeneratedPrompt({
              text: accentColor.prompt,
              category: 'Color',
              removable: true
            })
          }
        },

        // Backdrop Color
        setBackgroundColor: (colorName: string) => {
          const backgroundColor = BACKGROUND_COLORS.find(c => c.name === colorName)
          set({ backgroundColor })
          
          if (backgroundColor) {
            get().addGeneratedPrompt({
              text: backgroundColor.prompt,
              category: 'Color',
              removable: true
            })
          }
        },

        // Border Color
        setBorderColor: (colorName: string) => {
          const borderColor = BORDER_COLORS.find(c => c.name === colorName)
          set({ borderColor })
          
          if (borderColor) {
            get().addGeneratedPrompt({
              text: borderColor.prompt,
              category: 'Color',
              removable: true
            })
          }
        },

        // Shadow
        setShadow: (shadowName: string) => {
          const shadow = SHADOWS.find(s => s.name === shadowName)
          set({ shadow })
          
          if (shadow) {
            get().addGeneratedPrompt({
              text: shadow.prompt,
              category: 'Shadow',
              removable: true
            })
          }
        },

        // Typography
        setTypefaceFamily: (familyName) => {
          const typefaceFamily = TYPEFACE_FAMILIES.find(tf => tf.name === familyName)
          set({ typefaceFamily })
          
          if (typefaceFamily) {
            get().addGeneratedPrompt({
              text: typefaceFamily.prompt,
              category: 'Typography',
              removable: true
            })
          }
        },

        setHeadingFont: (fontFamilyName: string) => {
          const headingFont = HEADING_FONT.find(hf => hf.name === fontFamilyName)
          set({ headingFont })
          
          if (headingFont) {
            get().addGeneratedPrompt({
              text: headingFont.prompt,
              category: 'Typography',
              removable: true
            })
          }
        },

        setBodyFont: (fontFamilyName: string) => {
          const bodyFont = BODY_FONT.find(bf => bf.name === fontFamilyName)
          set({ bodyFont })
          
          if (bodyFont) {
            get().addGeneratedPrompt({
              text: bodyFont.prompt,
              category: 'Typography',
              removable: true
            })
          }
        },

        setHeadingSize: (sizeName: string) => {
          const headingSize = HEADING_SIZE.find(hs => hs.name === sizeName)
          set({ headingSize })
          
          if (headingSize) {
            get().addGeneratedPrompt({
              text: headingSize.prompt,
              category: 'Typography',
              removable: true
            })
          }
        },

        setSubheadingSize: (sizeName: string) => {
          const subheadingSize = SUBHEADING_SIZE.find(ss => ss.name === sizeName)
          set({ subheadingSize })
          
          if (subheadingSize) {
            get().addGeneratedPrompt({
              text: subheadingSize.prompt,
              category: 'Typography',
              removable: true
            })
          }
        },

        setBodyTextSize: (sizeName: string) => {
          const bodyTextSize = BODY_TEXT_SIZE.find(bts => bts.name === sizeName)
          set({ bodyTextSize })
          
          if (bodyTextSize) {
            get().addGeneratedPrompt({
              text: bodyTextSize.prompt,
              category: 'Typography',
              removable: true
            })
          }
        },

        setHeadingFontWeight: (weightName: string) => {
          const headingFontWeight = HEADING_FONT_WEIGHT.find(hfw => hfw.name === weightName)
          set({ headingFontWeight })
          
          if (headingFontWeight) {
            get().addGeneratedPrompt({
              text: headingFontWeight.prompt,
              category: 'Typography',
              removable: true
            })
          }
        },

        setHeadingLetterSpacing: (spacingName: string) => {
          const headingLetterSpacing = HEADING_LETTER_SPACING.find(hls => hls.name === spacingName)
          set({ headingLetterSpacing })
          
          if (headingLetterSpacing) {
            get().addGeneratedPrompt({
              text: headingLetterSpacing.prompt,
              category: 'Typography',
              removable: true
            })
          }
        },

        // Animation
        addAnimationType: (animationTypeName) => {
          const animationType = ANIMATION_TYPES.find(at => at.name === animationTypeName)
          if (animationType) {
            set(state => ({
              animationType: [...state.animationType, animationType]
            }))
            
            get().addGeneratedPrompt({
              text: animationType.prompt,
              category: 'Animation',
              removable: true
            })
          }
        },

        removeAnimationType: (animationTypeName) => {
          set(state => ({
            animationType: state.animationType.filter(at => at.name !== animationTypeName)
          }))
          
          // Remove related prompt
          const state = get()
          const promptToRemove = state.generatedPrompts.find(p => 
            p.text.includes(animationTypeName.toLowerCase()) && p.category === 'Animation'
          )
          if (promptToRemove) {
            get().removeGeneratedPrompt(promptToRemove.id)
          }
        },

        setAnimationDuration: (duration) => {
          set({ animationDuration: duration })
          
          get().addGeneratedPrompt({
            text: `Set animation duration to ${duration}s`,
            category: 'Animation',
            removable: true
          })
        },

        setAnimationDelay: (delay) => {
          set({ animationDelay: delay })
          
          if (delay > 0) {
            get().addGeneratedPrompt({
              text: `Set animation delay to ${delay}s`,
              category: 'Animation',
              removable: true
            })
          }
        },

        setAnimationTiming: (timing: AnimationTiming) => {
          set({ animationTiming: timing })
          
          get().addGeneratedPrompt({
            text: `Set animation timing to ${timing}`,
            category: 'Animation',
            removable: true
          })
        },

        setAnimationIterations: (iterations: AnimationIteration) => {
          set({ animationIterations: iterations })
          
          get().addGeneratedPrompt({
            text: `Set animation iterations to ${iterations}`,
            category: 'Animation',
            removable: true
          })
        },

        setAnimationDirection: (direction: AnimationDirection) => {
          set({ animationDirection: direction })
          
          get().addGeneratedPrompt({
            text: `Set animation direction to ${direction}`,
            category: 'Animation',
            removable: true
          })
        },

        // Generated Prompts
        addGeneratedPrompt: (prompt) => {
          const id = `prompt-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
          const newPrompt = { ...prompt, id }
          
          set(state => {
            // Remove existing prompt of same category if it exists
            const filtered = state.generatedPrompts.filter(p => 
              !(p.category === prompt.category && p.removable)
            )
            return {
              generatedPrompts: [...filtered, newPrompt]
            }
          })
        },

        removeGeneratedPrompt: (id) => {
          set(state => ({
            generatedPrompts: state.generatedPrompts.filter(p => p.id !== id)
          }))
        },

        updateGeneratedPrompt: (id, text) => {
          set(state => ({
            generatedPrompts: state.generatedPrompts.map(p => 
              p.id === id ? { ...p, text } : p
            )
          }))
        },

        // Utility
        reset: () => {
          set({ 
            ...initialState,
            generatedPrompts: []
          })
        },

        exportConfig: () => {
          const state = get()
          return JSON.stringify({
            platform: state.platform,
            layoutType: state.layoutType?.name,
            layoutConfiguration: state.layoutConfiguration?.name,
            style: state.style?.name,
            theme: state.theme?.name,
            accentColor: state.accentColor?.name,
            typefaceFamily: state.typefaceFamily?.name,
            animationType: state.animationType.map(at => at.name),
            animationDuration: state.animationDuration,
            animationDelay: state.animationDelay,
            generatedPrompts: state.generatedPrompts
          }, null, 2)
        },

        importConfig: (config) => {
          try {
            const parsed = JSON.parse(config)
            set({ 
              ...initialState,
              generatedPrompts: parsed.generatedPrompts || []
            })
            
            // Re-apply selections to trigger prompt generation
            if (parsed.layoutType) get().setLayoutType(parsed.layoutType)
            if (parsed.style) get().setStyle(parsed.style)
            if (parsed.theme) get().setTheme(parsed.theme)
            if (parsed.accentColor) get().setAccentColor(parsed.accentColor)
            if (parsed.typefaceFamily) get().setTypefaceFamily(parsed.typefaceFamily)
          } catch (error) {
            console.error('Failed to import config:', error)
          }
        },

        generateFinalPrompt: () => {
          const state = get()
          const prompts = state.generatedPrompts.map(p => p.text)
          
          // Add platform prefix
          const platformPrefix = state.platform === 'mobile' ? 'For mobile:' : 'For web:'
          
          return [platformPrefix, ...prompts].join('. ') + '.'
        }
      }),
      {
        name: 'prompt-builder-storage',
        partialize: (state) => ({
          platform: state.platform,
          generatedPrompts: state.generatedPrompts,
          // Don't persist the full objects to avoid stale references
          layoutType: state.layoutType?.name,
          style: state.style?.name,
          theme: state.theme?.name,
          accentColor: state.accentColor?.name,
          typefaceFamily: state.typefaceFamily?.name,
          animationType: state.animationType.map(at => at.name),
          animationDuration: state.animationDuration,
          animationDelay: state.animationDelay,
        })
      }
    ),
    { name: 'prompt-builder' }
  )
)