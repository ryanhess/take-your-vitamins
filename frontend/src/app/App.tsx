import { useState, useRef, useEffect } from "react";
import { X, Menu } from "lucide-react";
import herbsImage from "../imports/brooke-lark-kXQ3J7_2fpc-unsplash.jpg";

type SupplementResponseType = {
  name: string;
  before_after_food: "before" | "after";
  take_not_with: string[];
  DEV_conflict_count: number;
};

type Schedule = {
  before_breakfast: string[];
  after_breakfast: string[];
  before_lunch: string[];
  after_lunch: string[];
  before_dinner: string[];
  after_dinner: string[];
};

const THEMES = {
  "Soft Linen": {
    bg: "bg-gradient-to-br from-white to-[#f9f6f1]",
    input: "bg-white border-white focus:border-white focus:ring-0",
    suggestion: "bg-[#f0ebe3] text-[#5a4f42]",
    card: "bg-[#ffffff] border-[#e8e0d5]",
    text: "text-[#5a4f42]",
    title: "text-[#5a4030]",
    useImage: false,
  },
  "Textured Linen": {
    bg: "#f5f0e8",
    bgImage:
      "url(https://images.unsplash.com/photo-1775369351415-9ecfe51eb07b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=2000)",
    bgImageOpacity: 0.25,
    input:
      "bg-white border-white focus:border-black focus:ring-4 focus:ring-[#f5f0e8]",
    suggestion: "bg-[#f0ebe3] text-[#5a4f42]",
    card: "bg-[#ffffff] border-[#e8e0d5]",
    text: "text-[#5a4f42]",
    title: "text-black",
    useImage: true,
  },
  "Natural Herbs": {
    bg: "#f8f6f2",
    bgImage: `url(${herbsImage})`,
    bgImageOpacity: 0.3,
    input:
      "bg-white/90 border-white focus:border-white focus:ring-0 backdrop-blur-sm",
    suggestion: "bg-white/90 text-[#4a5d3f] backdrop-blur-sm",
    card: "bg-white/90 border-white/50 backdrop-blur-sm",
    text: "text-[#4a5d3f]",
    title: "text-black",
    useImage: true,
  },
};

const validSupplementNames = [
  "Vitamin A",
  "Vitamin B1",
  "Vitamin B2",
  "Vitamin B3",
  "Vitamin B5",
  "Vitamin B6",
  "Vitamin B7",
  "Vitamin B9",
  "Vitamin B12",
  "Vitamin C",
  "Vitamin D",
  "Vitamin D3",
  "Vitamin E",
  "Vitamin K",
  "Vitamin K2",
  "Calcium",
  "Iron",
  "Magnesium",
  "Zinc",
  "Potassium",
  "Selenium",
  "Copper",
  "Manganese",
  "Chromium",
  "Molybdenum",
  "Iodine",
  "Omega-3",
  "Fish Oil",
  "CoQ10",
  "Probiotics",
  "Collagen",
  "Ashwagandha",
  "Turmeric",
  "Curcumin",
  "Ginseng",
  "Ginkgo Biloba",
  "Echinacea",
  "St. John's Wort",
  "Melatonin",
  "L-Theanine",
  "Creatine",
  "Protein Powder",
  "BCAA",
  "Glucosamine",
  "Chondroitin",
  "MSM",
];

const URLS = {
  backend: (() => {
    const base = "/backend";
    return {
      getSchedule: `${base}/`,
    };
  })(),
} as const;

// Mock API: Generate new schedule from a list of vitamins
async function generateScheduleAPI(
  vitamins: Record<string, string>[],
): Promise<any | null> {
  const requestJSON = JSON.stringify(vitamins);
  const response = await fetch(URLS.backend.getSchedule, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: requestJSON,
  });
  if (!response.ok) {
    const errorBody = await response.json();
    console.error("generateSchedule failed:", response.status, errorBody);
    return null;
  }
  return response.json();
}

// Mock API: Update existing schedule
async function updateScheduleAPI(schedule: Schedule): Promise<void> {
  // TODO: Replace with real API call
  // await fetch('/api/schedule/update', {
  //   method: 'PUT',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ schedule })
  // });

  console.log("Schedule updated:", schedule);
}

export default function App() {
  const [input, setInput] = useState("");
  const [supplementSchedule, setSupplementSchedule] = useState<Schedule>({
    before_breakfast: [],
    after_breakfast: [],
    before_lunch: [],
    after_lunch: [],
    before_dinner: [],
    after_dinner: [],
  });
  const [suggestions, setSuggestions] = useState<string[]>(
    validSupplementNames.slice(0, 3),
  );
  const [suggestionStartIndex, setSuggestionStartIndex] = useState(3);
  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const [autocompleteSuggestion, setAutocompleteSuggestion] = useState("");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const hasEverHadSupplements = useRef(false);

  const theme = THEMES["Natural Herbs"];

  useEffect(() => {
    if (input.trim()) {
      const filtered = validSupplementNames.filter((supp) =>
        supp.toLowerCase().startsWith(input.toLowerCase()),
      );

      // Set autocomplete suggestion (first match)
      if (filtered.length > 0) {
        setAutocompleteSuggestion(filtered[0]);
      } else {
        setAutocompleteSuggestion("");
      }
    } else {
      setAutocompleteSuggestion("");
    }
  }, [input]);

  // Debounced effect for updating dropdown suggestions
  useEffect(() => {
    const timer = setTimeout(() => {
      if (input.trim()) {
        const filtered = validSupplementNames
          .filter((supp) => supp.toLowerCase().includes(input.toLowerCase()))
          .slice(0, 3);
        setSuggestions(filtered);
        setHighlightedIndex(0);
      } else {
        setSuggestions(validSupplementNames.slice(0, 3));
        setHighlightedIndex(0);
      }
    }, 100);

    return () => clearTimeout(timer);
  }, [input]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setHighlightedIndex((prev) =>
        prev < suggestions.length - 1 ? prev + 1 : prev,
      );
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev > 0 ? prev - 1 : 0));
    } else if (e.key === "Tab" && autocompleteSuggestion) {
      e.preventDefault();
      addVitamin(autocompleteSuggestion);
    } else if (e.key === "Enter" && suggestions.length > 0) {
      e.preventDefault();
      addVitamin(suggestions[highlightedIndex]);
    }
  };

  const getScheduleFromResponse = (resp: any): Schedule => {
    const scheduleFromResponse = resp.schedule;
    const responseSchedKVPairs = Object.entries(scheduleFromResponse);
    const newSchedule: Schedule = Object.fromEntries(
      responseSchedKVPairs.map(([timeSlot, sups]) => [
        timeSlot,
        sups.map((sup: any) => sup.name),
      ]),
    );
    return newSchedule;
  };

  const addVitamin = async (
    newSupplement: string,
    fromPill: boolean = false,
  ) => {
    const currentScheduleNames = Object.values(supplementSchedule).flat();

    const newSupplementNames = [...currentScheduleNames, newSupplement];

    const supplementRequestObjs = newSupplementNames.map((supName) => ({
      name: supName,
    }));

    const response = await generateScheduleAPI(supplementRequestObjs);
    if (!response) return;

    const newSchedule = getScheduleFromResponse(response);
    setSupplementSchedule(newSchedule);

    hasEverHadSupplements.current = true;

    // Check if the vitamin is in current suggestions and replace it
    const newSuggestions = [...suggestions];
    const vitaminIndex = newSuggestions.indexOf(newSupplement);

    if (vitaminIndex !== -1) {
      // Find next available supplement not in selected or current suggestions
      let nextSupplement = null;
      let searchIndex = suggestionStartIndex;

      while (searchIndex < validSupplementNames.length && !nextSupplement) {
        const candidate = validSupplementNames[searchIndex];
        if (
          !currentScheduleNames.includes(candidate) &&
          !suggestions.includes(candidate) &&
          candidate !== newSupplement
        ) {
          nextSupplement = candidate;
        }
        searchIndex++;
      }

      if (nextSupplement) {
        newSuggestions[vitaminIndex] = nextSupplement;
        setSuggestions(newSuggestions);
        setSuggestionStartIndex(searchIndex);
      }
    }

    setInput("");
    setAutocompleteSuggestion("");
    inputRef.current?.focus();
  };

  const removeVitaminFromSchedule = async (
    vitamin: string,
    slot: keyof Schedule,
  ) => {
    // Optimistically update UI
    const newSchedule = {
      ...supplementSchedule,
      [slot]: supplementSchedule[slot].filter((v) => v !== vitamin),
    };
    setSupplementSchedule(newSchedule);

    // Call API to update existing schedule
    await updateScheduleAPI(newSchedule);
  };

  return (
    <div
      className={`size-full overflow-y-auto relative ${!theme.useImage ? theme.bg : ""}`}
    >
      {theme.useImage && (
        <>
          <div
            className="absolute inset-0 z-0"
            style={{
              backgroundColor: theme.bg,
            }}
          />
          <div
            className="absolute inset-0 z-1"
            style={{
              backgroundImage: theme.bgImage,
              backgroundSize: "cover",
              backgroundPosition: "center",
              backgroundRepeat: "no-repeat",
              opacity: theme.bgImageOpacity,
              filter: "brightness(1.1) contrast(0.8)",
            }}
          />
        </>
      )}
      <div className="relative z-10 size-full overflow-y-auto">
        <nav className="w-full sm:border-b border-black/10 relative">
          <div className="max-w-6xl mx-auto px-8 py-4 flex items-center justify-between">
            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-8">
              <button className="text-sm hover:text-[#b49b57] transition-colors">
                About
              </button>
              <button className="text-sm hover:text-[#b49b57] transition-colors">
                Resources
              </button>
              <button className="text-sm hover:text-[#b49b57] transition-colors">
                My Schedule
              </button>
            </div>
            <button className="hidden md:block text-sm font-semibold hover:text-[#b49b57] transition-colors">
              Log In
            </button>

            {/* Mobile Hamburger */}
            <button
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle menu"
            >
              <Menu size={24} />
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden absolute top-full left-0 right-0 border-t border-black/10 bg-white/95 backdrop-blur-sm shadow-lg z-50">
              <div className="px-8 py-6 flex flex-col gap-5">
                <button className="text-base text-left hover:text-[#b49b57] transition-colors">
                  About
                </button>
                <button className="text-base text-left hover:text-[#b49b57] transition-colors">
                  Resources
                </button>
                <button className="text-base text-left hover:text-[#b49b57] transition-colors">
                  My Schedule
                </button>
                <button className="text-base font-semibold text-left hover:text-[#b49b57] transition-colors pt-3 border-t border-black/10">
                  Log In
                </button>
              </div>
            </div>
          )}
        </nav>
        <div className="w-full max-w-2xl mx-auto pt-0 sm:pt-24 px-8">
          <h1
            className={`${theme.title} text-3xl sm:text-5xl font-extrabold mb-2 text-center`}
          >
            Vitamin Scheduler
          </h1>
          <p className={`${theme.text} text-center mb-8 italic`}>
            Enter your supplements and a schedule will appear below.
          </p>

          <div className="relative">
            <div className="relative">
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Start typing a supplement name..."
                className={`w-full px-4 sm:px-6 py-3 sm:py-4 text-base sm:text-xl border-2 ${theme.input} rounded-2xl shadow-lg focus:outline-none transition-all relative`}
                autoFocus
              />
              {autocompleteSuggestion && input && (
                <div className="absolute inset-0 px-4 sm:px-6 py-3 sm:py-4 pointer-events-none flex items-center text-base sm:text-xl">
                  <div className="text-gray-300 whitespace-pre">
                    <span className="opacity-0">{input}</span>
                    <span
                      className="inline-block"
                      style={{ width: "0.15ch" }}
                    ></span>
                    {autocompleteSuggestion.slice(input.length)}
                  </div>
                </div>
              )}
            </div>

            {input && (
              <div className="absolute left-2.5 right-2.5 top-full -mt-1 bg-white rounded-lg shadow-lg overflow-hidden z-20">
                {suggestions.map((suggestion, index) => (
                  <button
                    key={suggestion}
                    onClick={() => addVitamin(suggestion, true)}
                    className={`w-full text-left px-4 py-2.5 transition-colors border-b border-gray-100 last:border-b-0 ${
                      index === highlightedIndex
                        ? "bg-gray-100 text-[#b49b57]"
                        : "text-gray-400 hover:bg-gray-50 hover:text-[#b49b57]"
                    }`}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}

            <div className="flex flex-wrap sm:flex-nowrap justify-center gap-2 mt-4">
              {!input &&
                suggestions.map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => addVitamin(suggestion, true)}
                    className="px-3 sm:px-4 py-1.5 bg-white border border-gray-200 rounded-full text-xs sm:text-sm text-black hover:text-[#b49b57] transition-colors whitespace-nowrap"
                  >
                    {suggestion}
                  </button>
                ))}
            </div>
          </div>

          {hasEverHadSupplements.current && (
            <div
              className={`${theme.card} px-6 py-4 rounded-2xl shadow-md mt-8`}
            >
              {Object.values(supplementSchedule).every(
                (timeSlot) => timeSlot.length === 0,
              ) ? (
                <div className="text-gray-400 italic">
                  Schedule will appear here...
                </div>
              ) : (
                Object.entries(supplementSchedule).map(
                  ([slot, supplements], index, scheduleKVPairs) => {
                    if (supplements.length === 0) return null;

                    const isLast =
                      index ===
                      scheduleKVPairs.findLastIndex(
                        ([_, supps]) => supps.length > 0,
                      );

                    return (
                      <div key={slot}>
                        <h3 className={`${theme.text} font-bold text-lg mb-2`}>
                          {slot
                            .split("_")
                            .map(
                              (word) =>
                                word.charAt(0).toUpperCase() + word.slice(1),
                            )
                            .join(" ")}
                        </h3>
                        <hr className="border-gray-200 mb-3" />
                        <div className="flex flex-wrap gap-4">
                          {supplements.map((supplement) => (
                            <div
                              key={supplement}
                              className={`${theme.text} flex items-center gap-1 group`}
                            >
                              <span>{supplement}</span>
                              <X
                                size={14}
                                strokeWidth={3.5}
                                className="text-[#c24d3d] opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
                                onClick={() =>
                                  removeVitaminFromSchedule(
                                    supplement,
                                    slot as keyof Schedule,
                                  )
                                }
                              />
                            </div>
                          ))}
                        </div>
                        {!isLast && <div className="mb-6"></div>}
                      </div>
                    );
                  },
                )
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
