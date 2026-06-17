# Data Model (shared contracts)

Lives in `packages/contracts` and is imported by both `apps/web` and `apps/api`. These are the typed shapes for the whole product. Field names use the **technical** vocabulary from `glossary.md`.

> Reconcile with your technical spec's "durable contracts" before freezing field names — the spec is the authority on the exact agent-config and run-result schemas. These are a faithful, buildable starting point.

```ts
// ─── Identity ──────────────────────────────────────────────
export type SchoolId =
  | 'artificer' | 'tactician' | 'beastmaster'
  | 'loremaster' | 'ascetic' | 'wanderer';

export interface School {
  id: SchoolId;
  name: string;            // "Tactician"
  color: string;           // identity hex, e.g. "#5b8cff"
  specialty: string;       // "Strategy & Orchestration"
  lore: string;
}

export interface Architect {
  id: string;
  name: string;
  school: SchoolId;
  rank: Rank;
  record: WinLoss;
  treasury: number;        // display currency (Phase 0: mock)
  createdAt: string;
}

// ─── The six-layer Champion ────────────────────────────────
export type LayerKey =
  | 'persona' | 'tools' | 'memory' | 'strategy' | 'subAgents' | 'model';

export interface PersonaLayer { systemPrompt: string; }
export interface ToolsLayer   { equipped: string[]; }           // tool ids
export interface MemoryLayer  { knowledgePacks: string[]; fewShots: number; }
export interface StrategyLayer{
  plan: boolean; selfCritique: boolean; verify: boolean; maxRetries: number;
}
export interface SubAgentsLayer { specialists: string[]; }      // e.g. ["researcher","verifier"]
export interface ModelLayer   { model: string; }               // "claude-haiku-4-5"

export interface AgentConfig {
  persona: PersonaLayer;
  tools: ToolsLayer;
  memory: MemoryLayer;
  strategy: StrategyLayer;
  subAgents: SubAgentsLayer;
  model: ModelLayer;
}

export interface Champion {
  id: string;
  architectId: string;
  name: string;            // "Cartographer"
  epithet?: string;        // "the Methodical"
  spriteKind: 'hero' | 'knight' | 'core';
  color: string;
  config: AgentConfig;
  record: WinLoss;
  rank: Rank;
  badges: Badge[];         // archetype tags
}

export interface Badge { label: string; color: string; } // "TACTICS"

// ─── Catalog: a tool / item in the Armory ──────────────────
export interface ArmoryItem { id: string; name: string; cost: number; }
export interface LoadoutRules { budget: number; }          // e.g. 100

// ─── War formats & the Lock Matrix (configurability principle)
export type LockState = 'frozen' | 'free';
export type LockMatrix = Record<LayerKey, LockState>;

export interface WarFormat {
  id: string;
  name: string;            // "Loadout War"
  description: string;
  difficulty: 1|2|3|4|5;
  lockMatrix: LockMatrix;
  loadout?: LoadoutRules;  // present when tools are 'free'
  judging: JudgingSpec;
}

export interface JudgingSpec {
  // Phase 0 may stub this; keep the shape.
  autoChecks: boolean;     // objective pass/fail available
  llmJudge: boolean;       // quality judged by model from quoted evidence
  rubric?: string[];       // criteria, e.g. ["correctness","elegance","economy"]
}

// ─── A concrete, joinable war ──────────────────────────────
export type ContractStatus = 'open' | 'live' | 'closed';
export interface WarInstance {
  id: string;
  formatId: string;
  status: ContractStatus;
  opensAt: string; closesAt: string;
  reward: Reward;
  // sealed: the task is NEVER serialized to the client
  taskRef: string;         // opaque id; backend resolves to the sealed task
}

export interface Reward { gold: number; medal?: string; seasonPoints?: number; }

// ─── Submission → Run → Replay → Verdict ───────────────────
export interface Submission {
  id: string;
  warInstanceId: string;
  architectId: string;
  championId: string;
  configSnapshot: AgentConfig; // frozen at submit time (reproducibility)
  submittedAt: string;
}

export type RunStatus = 'queued' | 'running' | 'complete' | 'errored';
export interface Run {
  id: string;
  submissionId: string;
  status: RunStatus;
  model: string;           // resolved model + version actually used
  seed?: number;
  startedAt?: string; finishedAt?: string;
  budgetUsed?: number; budgetMax?: number;
}

// The watchable replay — what the Battle screen renders.
export type ReplayEventType =
  | 'narration' | 'tool_call' | 'subagent_spawn'
  | 'retry' | 'budget' | 'submit' | 'verdict';

export interface ReplayEvent {
  t: number;               // order / timestamp
  side: 'L' | 'R';
  type: ReplayEventType;
  who: string;             // "CARTOGRAPHER" | "— THE REFEREE —"
  text: string;            // narration shown in DialogueBox
  callout?: string;        // "STRIKE!" | "VAULT OPEN"
  budgetDelta?: number;    // % change to that fighter's bar
  hit?: boolean;           // trigger recoil + heavier spark burst
}

export interface Verdict {
  warInstanceId: string;
  scores: { championId: string; name: string; score: number }[];
  winnerId: string;
  rankDelta: number;       // e.g. Glicko +18
  reward: Reward;
}

// ─── Ladder / standings (Phase 0: mock/display) ────────────
export type Tier = 'Bronze'|'Silver'|'Gold'|'Platinum'|'Diamond'|'Champion';
export interface Rank { tier: Tier; division: number; rating?: number; }
export interface WinLoss { wins: number; losses: number; }
```

## Seed data

Provide a `packages/contracts/seed.ts` with: the six `School`s (colors/lore from `screens-spec.md`), the `ArmoryItem`s, the four `WarFormat`s + matching `WarInstance`s (lock matrices in `screens-spec.md`), the seed roster Champions, and a fallback `ReplayEvent[]` (the prototype `SCRIPT`). The frontend renders against this seed until the API is wired.

## Invariants (enforce, don't assume)

- A frozen layer in a `WarFormat.lockMatrix` **must** equal the format's shared value; the server rejects submissions that differ. The client may not edit frozen layers.
- `configSnapshot` on `Submission` is immutable once created.
- `WarInstance` never carries task content to the client (`taskRef` only).
- `Run.model` records the *actual* resolved model+version, not the requested one.
