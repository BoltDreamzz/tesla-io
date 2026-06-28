const { useState } = React;

function Onboarding() {

    const slides = [

        {
            title: "Welcome to QFX",

            subtitle:
                "The next generation secure digital financial platform.",

            image: "/static/home_media/welcome.svg",

            button: "Next"
        },

        {
            title: "Military Grade Security",

            subtitle:
                "Your transactions are encrypted and protected at all times.",

            image: "/static/home_media/security.svg",

            button: "Next"
        },

        {
            title: "You're Ready",

            subtitle:
                "Let's begin your financial journey with QFX.",

            image: "/static/home_media/rocket.svg",

            button: "Done"
        }

    ];

    const [current, setCurrent] = useState(0);

    const slide = slides[current];

    function next() {

        if (current < slides.length - 1) {

            setCurrent(current + 1);

        }
        else {

            alert("Redirecting...");

            window.location = "/qfs/cards/";

        }

    }

    function previous() {

        if (current > 0) {

            setCurrent(current - 1);

        }

    }

    function skip() {

        setCurrent(slides.length - 1);

    }

    function playAgain() {

        setCurrent(0);

    }

    return (

        <div
            className="h-screen w-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900 overflow-hidden">

            <div
                className="w-full max-w-4xl h-[85vh] rounded-3xl bg-white/10 backdrop-blur-xl shadow-2xl border border-white/20 p-10 flex flex-col">

                {/* Image */}

                <div
                    className="flex justify-center flex-1">

                    <img

                        src={slide.image}

                        className="w-72 object-contain" />

                </div>

                {/* Title */}

                <h1
                    className="text-center text-white text-5xl font-bold">

                    {slide.title}

                </h1>

                <p
                    className="text-center text-slate-300 mt-6 text-lg">

                    {slide.subtitle}

                </p>

                {/* Progress */}

                <div
                    className="flex justify-center gap-3 mt-12">

                    {

                        slides.map((item, index) => (

                            <div

                                key={index}

                                className={`

w-3

h-3

rounded-full

transition-all

duration-300

${index === current

                                        ?

                                        "bg-blue-500 scale-125"

                                        :

                                        "bg-gray-500"

                                    }

`}

                            />

                        ))

                    }

                </div>

                {/* Buttons */}

                <div
                    className="mt-auto flex justify-between">

                    <div>

                        {

                            current > 0 &&

                            <button

                                onClick={previous}

                                className="px-6 py-3 rounded-xl bg-slate-700 hover:bg-slate-600 text-white">

                                Back

                            </button>

                        }

                    </div>

                    <div
                        className="space-x-3">

                        {

                            current !== slides.length - 1 &&

                            <button

                                onClick={skip}

                                className="px-6 py-3 rounded-xl bg-transparent border border-gray-500 text-gray-300 hover:bg-gray-800">

                                Skip

                            </button>

                        }

                        <button

                            onClick={next}

                            className="px-8 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white">

                            {slide.button}

                        </button>

                    </div>

                </div>

                {

                    current === slides.length - 1 &&

                    <div
                        className="mt-8 text-center">

                        <button

                            onClick={playAgain}

                            className="text-blue-400 hover:text-blue-300">

                            ▶ Play Again

                        </button>

                    </div>

                }

            </div>

        </div>

    );

}

const root =
    document.getElementById("onboarding-root");

if (root) {

    if (!window.onboardingRoot) {

        window.activityFeedRoot =
            ReactDOM.createRoot(root);

    }

    window.onboardingRoot.render(
        <Onboarding />
    );
}