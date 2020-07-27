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
  (vec (for [state state-group] (step-state state shift))))

(def shift-pmf {:left 1/3 :stay 1/3 :right 1/3})

                                        ; This is probably overkill, now that I've written it.
(def transform-pmf
  (apply merge-with +
        (for [[shift,p] shift-pmf]
          {
           (fn [state-group] (step-state-group state-group shift))
           p
           }
          )
        ))

(defn conditioned-on-state-group [state-group]
  (into {}
        (for [[transform, probability] transform-pmf]
          [(transform state-group), probability]
          )
        )
  )

                                        ; It would be nice if this validated that the resulting PMF has sum(values) == 1
(defn sum-pmfs [& pmfs]
  (apply merge-with + pmfs)
  )

(defn scalar-mul-vals [c m]
  (into
   {}
   (for [[k,v] m] [k (* c v)])
   )
  )

(defn step-distribution [state-group-pmf]
  (as->
                                        ; Generate the set of conditional distributions.
      (vec (for [[state-group, p] state-group-pmf]
                                        ; Multiply them by the appropriate base probability.
             (scalar-mul-vals p (conditioned-on-state-group state-group))))
      v

                                        ; Merge all the conditional distributions.
    (apply sum-pmfs v)
    )
  )

(defn coalesced? [state-group]
  (= (count (set state-group)) 1)
  )

(defn p-coalesced [state-group-pmf]
  (as->
      (filter (fn [[state-group p]] (coalesced? state-group)) state-group-pmf)
      v

    (vals v)
    (apply + v)
    )
  )

(defn coalesced-pmf [state-group-pmf]
  (filter (fn [[state-group p]] (coalesced? state-group)) state-group-pmf))

(def start {[1,2,3] 1})
(loop [
       i 0
       state-group-pmf start
       ]

  (when
      (< i 5)
    (do
      (prn i
           "->"
           ;; (into {}
           ;;       (map
           ;;        (fn [[state-group, p]] [state-group, (float p)])
           ;;                              ; (coalesced-pmf state-group-pmf)
           ;;        state-group-pmf
           ;;        )
           ;;       )
           state-group-pmf
           (apply + (vals state-group-pmf))
           )
      (recur (inc i) (step-distribution state-group-pmf))
      )
    )
  )
