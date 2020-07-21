(def N 3)

(defn step-state [state shift]
    (case shift
        :left
        (if (> state 1) (dec state) state)

        :stay
        state

        :right
        (if (< state N) (inc state) state)
    )
)

(defn step-state-group [state-group shift]
    (for [state state-group] (step-state state shift)))

(def shift-pmf {:left 1/3 :stay 1/3 :right 1/3})

(def transform-pmf
    (into {}
        (for [[shift,p] shift-pmf]
            [
                (fn [state-group] (step-state-group state-group shift))
                p
            ]
        )
    ))