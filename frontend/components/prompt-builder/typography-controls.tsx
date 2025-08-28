'use client'

import { OptionCard } from '@/components/ui/option-card'
import { BODY_FONT, BODY_TEXT_SIZE, HEADING_FONT, HEADING_FONT_WEIGHT, HEADING_LETTER_SPACING, HEADING_SIZE, SUBHEADING_SIZE, TYPEFACE_FAMILIES } from '@/lib/prompt-builder-config'
import { usePromptBuilderStore } from '@/lib/stores/prompt-builder-store'

export function TypographyControls() {
  const { 
    typefaceFamily,
    headingFont,
    bodyFont,
    headingSize,
    subheadingSize,
    bodyTextSize,
    headingFontWeight,
    headingLetterSpacing,
    setTypefaceFamily,
    setHeadingFont,
    setBodyFont,
    setHeadingSize,
    setSubheadingSize,
    setBodyTextSize,
    setHeadingFontWeight,
    setHeadingLetterSpacing
  } = usePromptBuilderStore()

  return (
    <div className="space-y-6 overflow-hidden">
      {/* Font Family */}
      <div className="space-y-2">
        <h3 className="font-medium">Typeface Family</h3>
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {TYPEFACE_FAMILIES.map((family) => (
            <div key={family.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={family}
                isSelected={typefaceFamily?.name === family.name}
                onClick={() => setTypefaceFamily(family.name)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Heading Font */}
      <div className="space-y-2">
        <h3 className="font-medium">Heading Font</h3>
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {HEADING_FONT.map((font) => (
            <div key={font.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={font}
                isSelected={headingFont?.name === font.name}
                onClick={() => setHeadingFont(font.name)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Body Font */}
      <div className="space-y-2">
        <h3 className="font-medium">Body & UI Font</h3>
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {BODY_FONT.map((font) => (
            <div key={font.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={font}
                isSelected={bodyFont?.name === font.name}
                onClick={() => setBodyFont(font.name)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Heading Size */}
      <div className="space-y-2">
        <h3 className="font-medium">Heading Size</h3>
        <div className="flex gap-2 overflow-x-auto pb-3 -mx-4 px-4">
          {HEADING_SIZE.map((size) => (
            <div key={size.name} className="flex-shrink-0 w-16">
              <OptionCard
                option={size}
                isSelected={headingSize?.name === size.name}
                onClick={() => setHeadingSize(size.name)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Subheading Size */}
      <div className="space-y-2">
        <h3 className="font-medium">Subheading Size</h3>
        <div className="flex gap-2 overflow-x-auto pb-3 -mx-4 px-4">
          {SUBHEADING_SIZE.map((size) => (
            <div key={size.name} className="flex-shrink-0 w-16">
              <OptionCard
                option={size}
                isSelected={subheadingSize?.name === size.name}
                onClick={() => setSubheadingSize(size.name)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Body Text Size */}
      <div className="space-y-2">
        <h3 className="font-medium">Body Text Size</h3>
        <div className="flex gap-2 overflow-x-auto pb-3 -mx-4 px-4">
          {BODY_TEXT_SIZE.map((size) => (
            <div key={size.name} className="flex-shrink-0 w-16">
              <OptionCard
                option={size}
                isSelected={bodyTextSize?.name === size.name}
                onClick={() => setBodyTextSize(size.name)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Heading Font Weight */}
      <div className="space-y-2">
        <h3 className="font-medium">Heading Font Weight</h3>
        <div className="flex gap-2 overflow-x-auto pb-3 -mx-4 px-4">
          {HEADING_FONT_WEIGHT.map((weight) => (
            <div key={weight.name} className="flex-shrink-0 w-16">
              <OptionCard
                option={weight}
                isSelected={headingFontWeight?.name === weight.name}
                onClick={() => setHeadingFontWeight(weight.name)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Heading Letter Spacing */}
      <div className="space-y-2">
        <h3 className="font-medium">Heading Letter Spacing</h3>
        <div className="flex gap-2 overflow-x-auto pb-3 -mx-4 px-4">
          {HEADING_LETTER_SPACING.map((spacing) => (
            <div key={spacing.name} className="flex-shrink-0 w-16">
              <OptionCard
                option={spacing}
                isSelected={headingLetterSpacing?.name === spacing.name}
                onClick={() => setHeadingLetterSpacing(spacing.name)}
              />
            </div>
          ))}
        </div>
      </div>
      

      {/* Font Preview */}
      {typefaceFamily && (
        <div className="p-4 rounded-lg bg-muted/30 border-2 border-dashed border-muted-foreground/20">
          <h4 className="text-sm font-medium mb-2 text-muted-foreground">Preview</h4>
          <div 
            className={`text-lg ${
              typefaceFamily.name === 'Sans' ? 'font-sans' :
              typefaceFamily.name === 'Serif' ? 'font-serif' :
              typefaceFamily.name === 'Monospace' ? 'font-mono' : 'font-sans'
            }`}
          >
            <div className="text-2xl font-bold mb-2">Heading Text</div>
            <div className="text-base text-muted-foreground">
              This is how your selected typography will appear in your design. 
              The quick brown fox jumps over the lazy dog.
            </div>
          </div>
        </div>
      )}

      <div className="text-xs text-muted-foreground">
        More typography options like font sizes, weights, and spacing will be added in future updates.
      </div>
    </div>
  )
}