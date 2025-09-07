import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/misc-components"; // or your Badge
import { Progress } from "@/components/ui/progress"; // if you have one; fallback provided below
import { cn } from "@/lib/utils";
import { Check, Clock, Layout, ListChecks, Monitor, Palette, Settings2 } from "lucide-react";
import { useMemo, useState } from "react";

/**
 * Drop-in UI renderers for your /chat event-stream phases.
 * Works with the metadata you're already attaching in sendMessageStreaming.applyFrame().
 *
 * Usage (minimal):
 *  - In ChatHistory, when the message.type === 'ai' && message.metadata?.phase, render <AiMessageRenderer ... />
 *  - Keep using MessageBubble for user messages and plain AI text for ConversationPhase.INITIAL.
 */

export type GeneratedScreen = {
    id: string
    title: string
    screen_type: string
    html?: string
    css?: string
    js?: string
    description?: string
    components?: string[]
    generated_at?: string
}

export type DesignPlan = {
    screens: Array<{
        id: string
        screen_type: string
        title: string
        description?: string
        priority?: number
        order?: number
        components?: string[]
        interactions?: string[]
        data_requirements?: string[]
    }>
    design_system?: {
        color_scheme?: string
        primary_color?: string
        typography?: string
        spacing?: string
    }
    generation_strategy?: string
    estimated_complexity?: string
    target_devices?: string[]
}

export type GenerationProgress = {
    current_screen?: number
    total_screens?: number
    overall_progress?: number // 0-100
    current_screen_name?: string
    current_screen_id?: string
    status?: "queued" | "running" | "completed" | string
}

export type AiMeta = {
    phase?: string
    requiresApproval?: boolean
    designPlan?: DesignPlan
    generationProgress?: GenerationProgress
    generatedScreens?: GeneratedScreen[]
    humanFeedback?: any
}

export function AiMessageRenderer({
    responseText,
    meta,
    onApprove,
    onRequestChanges,
}: {
    responseText?: string
    meta: AiMeta
    onApprove?: () => void
    onRequestChanges?: () => void
}) {
    const phase = normalizePhase(meta.phase)

    if (phase === "initial") {
        // Simple text bubble — parent can render normally. Keeping here for completeness.
        return (
            <div className="prose prose-sm max-w-none">{responseText}</div>
        )
    }

    if (phase === "awaiting_approval") {
        return (
            <AwaitingApprovalPanel
                responseText={responseText}
                designPlan={meta.designPlan}
                requiresApproval={!!meta.requiresApproval}
                onApprove={onApprove}
                onRequestChanges={onRequestChanges}
            />
        )
    }

    if (phase === "generating") {
        return (
            <GenerationProgressPanel
                responseText={responseText}
                progress={meta.generationProgress}
                plan={meta.designPlan}
            />
        )
    }

    if (phase === "complete") {
        return (
            <CompletePanel
                responseText={responseText}
                plan={meta.designPlan}
                progress={meta.generationProgress}
                screens={meta.generatedScreens}
            />
        )
    }

    // Fallback for any other phases
    return (
        <Card className="p-4">
            <div className="text-sm text-muted-foreground mb-2">Phase: {meta.phase}</div>
            {responseText && <div className="prose prose-sm max-w-none">{responseText}</div>}
        </Card>
    )
}

function normalizePhase(raw?: string) {
    const v = (raw || "").toLowerCase()
    if (v.includes("initial")) return "initial"
    if (v.includes("await") || v.includes("approval")) return "awaiting_approval"
    if (v.includes("generat")) return "generating"
    if (v.includes("complete")) return "complete"
    return v || "initial"
}

/** AWAITING APPROVAL */
function AwaitingApprovalPanel({
    responseText,
    designPlan,
    requiresApproval,
    onApprove,
    onRequestChanges,
}: {
    responseText?: string
    designPlan?: DesignPlan
    requiresApproval: boolean
    onApprove?: () => void
    onRequestChanges?: () => void
}) {
    return (
        <div className="space-y-4">
            {responseText && (
                <div className="rounded-xl border bg-white p-4 text-sm flex items-start gap-2">
                    <Clock className="h-4 w-4 mt-0.5" />
                    <div className="prose prose-sm max-w-none">{responseText}</div>
                </div>
            )}

            {designPlan && <DesignPlanSummary plan={designPlan} />}

            {requiresApproval && (
                <div className="flex items-center gap-3">
                    <Button size="sm" onClick={onApprove}>
                        <Check className="h-4 w-4 mr-1" /> Approve plan
                    </Button>
                    <Button size="sm" variant="outline" onClick={onRequestChanges}>
                        <ListChecks className="h-4 w-4 mr-1" /> Request changes
                    </Button>
                </div>
            )}
        </div>
    )
}

function DesignPlanSummary({ plan }: { plan: DesignPlan }) {
    return (
        <Card className="p-4">
            <div className="flex items-center justify-between mb-3">
                <div className="font-medium flex items-center gap-2">
                    <Layout className="h-4 w-4" /> Planned screens
                </div>
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    {plan.design_system?.primary_color && (
                        <Badge>{`Primary: ${plan.design_system.primary_color}`}</Badge>
                    )}
                    {plan.design_system?.typography && (
                        <Badge variant="outline">{plan.design_system.typography}</Badge>
                    )}
                    {plan.estimated_complexity && (
                        <Badge variant="outline">{plan.estimated_complexity}</Badge>
                    )}
                </div>
            </div>

            <div className="grid gap-3">
                {plan.screens?.sort((a, b) => (a.order ?? 0) - (b.order ?? 0)).map((s) => (
                    <div key={s.id} className="rounded-lg border p-3 bg-white">
                        <div className="flex items-center justify-between gap-2">
                            <div className="font-medium">{s.title}</div>
                            <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                <Badge variant="secondary">{s.screen_type}</Badge>
                                {typeof s.priority === "number" && <Badge variant="outline">prio {s.priority}</Badge>}
                                {typeof s.order === "number" && <Badge variant="outline">#{s.order}</Badge>}
                            </div>
                        </div>
                        {s.description && (
                            <p className="text-xs text-muted-foreground mt-1">{s.description}</p>
                        )}
                        <div className="mt-2 flex flex-wrap gap-1">
                            {(s.components || []).map((c) => (
                                <Badge key={c} variant="outline" className="text-[10px]">{c}</Badge>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-4 flex items-center gap-2 text-xs text-muted-foreground">
                <Palette className="h-4 w-4" />
                <span>
                    {plan.design_system?.color_scheme ?? "light"} · {plan.design_system?.spacing ?? "comfortable"}
                </span>
                <span className="mx-1">•</span>
                <span>Targets: {(plan.target_devices || []).join(", ") || "desktop"}</span>
            </div>
        </Card>
    )
}

/** GENERATING */
function GenerationProgressPanel({
    responseText,
    progress,
    plan,
}: {
    responseText?: string
    progress?: GenerationProgress
    plan?: DesignPlan
}) {
    const pct = clamp(progress?.overall_progress ?? 0, 0, 100)
    const subtitle = progress?.status === "completed"
        ? "Completed"
        : `Building ${progress?.current_screen_name || "…"} (${progress?.current_screen}/${progress?.total_screens})`

    return (
        <Card className="p-4">
            <div className="flex items-center justify-between mb-2">
                <div className="font-medium flex items-center gap-2"><Settings2 className="h-4 w-4" />Generating screens</div>
                {plan?.screens && (
                    <div className="text-xs text-muted-foreground">{plan.screens.length} planned</div>
                )}
            </div>
            {responseText && (
                <p className="text-sm text-muted-foreground mb-2">{responseText}</p>
            )}
            <Progress value={pct} className="h-2" />
            <div className="mt-2 text-xs text-muted-foreground">{subtitle}</div>
        </Card>
    )
}

/** COMPLETE */
function CompletePanel({
    responseText,
    plan,
    progress,
    screens,
}: {
    responseText?: string
    plan?: DesignPlan
    progress?: GenerationProgress
    screens?: GeneratedScreen[]
}) {
    const [activeId, setActiveId] = useState<string | undefined>(screens?.[0]?.id)
    const active = useMemo(() => screens?.find(s => s.id === activeId), [screens, activeId])


    return (
        <div className="space-y-4">
            {plan && <DesignPlanSummary plan={plan} />}
            <Card className="p-4 w-full">
                <div className="flex items-center justify-between">
                    <div className="font-medium flex items-center gap-2">
                        <Monitor className="h-4 w-4" /> Generated UI
                    </div>
                    <div className="text-xs text-muted-foreground">
                        {progress?.overall_progress ?? 100}% complete • {screens?.length || 0} screens
                    </div>
                </div>
                {responseText && (
                    <p className="text-sm text-muted-foreground mt-1">{responseText}</p>
                )}


                {/* Tabs */}
                {screens && screens.length > 0 && (
                    <div className="mt-3">
                        <div className="flex flex-wrap gap-2">
                            {screens.map((s) => (
                                <button
                                    key={s.id}
                                    onClick={() => setActiveId(s.id)}
                                    className={cn(
                                        "rounded-full border px-3 py-1 text-xs",
                                        activeId === s.id ? "bg-primary text-primary-foreground" : "bg-white hover:bg-muted"
                                    )}
                                    title={s.description || s.title}
                                >{s.title}</button>
                            ))}
                        </div>


                        {/* Live Preview */}
                        <div className="mt-3 rounded-xl border overflow-hidden bg-white">
                            {active ? (
                                <SafePreviewIframe screen={active} />
                            ) : (
                                <div className="p-6 text-sm text-muted-foreground">Select a screen to preview.</div>
                            )}
                        </div>
                    </div>
                )}
            </Card>



        </div>
    )
}


/** Live, sandboxed preview of generated HTML (no code blocks). */
function SafePreviewIframe({ screen, tight = false }: { screen: GeneratedScreen; tight?: boolean }) {
    const srcDoc = composeSrcDoc(screen) //useMemo(() => composeSrcDoc(screen), [screen])
    console.log(srcDoc)
    return (
        <iframe
            title={screen.title}
            className={cn("w-full", tight ? "h-64" : "h-[70vh]")}
            sandbox="allow-scripts allow-same-origin"
            srcDoc={srcDoc}
        />
    )
}

function composeSrcDoc(s: GeneratedScreen) {
    const raw = s.html || ""

    // Prefer the first ```html fenced block; fall back to the first fenced block; else raw string.
    const labeled = raw.match(/```(?:html|HTML)[ \t]*\r?\n([\s\S]*?)```/)
    const any = !labeled && raw.match(/```[ \t]*[a-zA-Z0-9_-]*[ \t]*\r?\n([\s\S]*?)```/)
    const extracted = (labeled ? labeled[1] : (any ? any[1] : "")).trim()

    const source = extracted || raw
    const tailwindTag = `<script src="https://cdn.tailwindcss.com"></script>`

    // If a full HTML doc was provided, inject/move Tailwind so it's the last tag in <head>
    if (/<!doctype/i.test(source)) {
        let out = source

        if (/<\/head>/i.test(out)) {
            // Remove any existing Tailwind script tags
            out = out.replace(
                /<script[^>]*src=["']https:\/\/cdn\.tailwindcss\.com["'][^>]*><\/script>\s*/gi,
                ""
            )
            // Insert Tailwind just before </head>
            out = out.replace(/<\/head>/i, `  ${tailwindTag}\n</head>`)
        }
        // If there's no </head>, we leave the document as-is (can't place it "at end of head")
        return out
    }

    // Otherwise, we compose a minimal doc and put Tailwind at the end of <head>
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
      ${tailwindTag}
    </head>
    <body>
    ${source || '<div class="p-6 text-sm text-gray-500">No HTML provided</div>'}
    </body>
    </html>`
}

function clamp(v: number, lo: number, hi: number) { return Math.max(lo, Math.min(hi, v)) }

