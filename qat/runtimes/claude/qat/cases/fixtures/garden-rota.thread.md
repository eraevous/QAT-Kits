# Community garden watering rota
<!-- Constructed test thread for thread-map evals (authored 2026-11-16 by claude:qat). Not a real conversation. Participants: Zach (user), Claude (assistant). -->

### Zach said:
<!-- T1 · 2026-09-14 10:02 -->
Our community garden has twenty-two plots and about thirty volunteers. Watering in summer is a mess: some beds get watered twice a day, some not at all. I'd like a simple way to run a watering rota. What would you suggest?

### Claude said:
<!-- T1 · 2026-09-14 10:03 -->
At that size a shared calendar with recurring slots would work, or a one-page web app that shows today's slot and lets the volunteer tick it off. The app gives you a record of who actually watered. Which matters more to you: a record, or the least effort to set up?

### Zach said:
<!-- T2 · 2026-09-14 10:09 -->
A record matters. One hard requirement though: it has to work without any login or account. Half our volunteers are over seventy and will not create a password for this. They should be able to open a link and tap their name.

### Claude said:
<!-- T2 · 2026-09-14 10:10 -->
Understood: no login, open a link and tap a name. A single page with the slot list and name buttons does that. The trade-off is that anyone with the link can tick for anyone, which is fine for a garden.

### Zach said:
<!-- T3 · 2026-09-14 10:15 -->
Fine with that. Let's make the rota weekly: each volunteer gets one fixed day per week.

### Claude said:
<!-- T3 · 2026-09-14 10:16 -->
Weekly fixed days, then. With thirty volunteers and seven days that is four or five people per day, so I'd let each day's group split morning and evening.

### Zach said:
<!-- T4 · 2026-09-14 10:31 -->
Different question while I think of it. Someone suggested soil moisture sensors in a few beds so we only water when it's dry. Is that worth it for a garden like ours?

### Claude said:
<!-- T4 · 2026-09-14 10:33 -->
Cheap capacitive sensors cost a few pounds each and work for a season or two. For twenty-two plots you would sample, say, four representative beds. The honest benefit is less over-watering in wet weeks; the cost is someone checking batteries. I could add a moisture reading to the rota page later.

### Zach said:
<!-- T5 · 2026-09-14 10:40 -->
Maybe next year. Not now.

### Claude said:
<!-- T5 · 2026-09-14 10:41 -->
Noted: sensors parked for next year.

### Zach said:
<!-- T6 · 2026-09-14 11:05 -->
Back to the rota. I talked to two of the regulars and weekly is too much for people. Switch it to fortnightly: each volunteer gets one fixed day every two weeks.

### Claude said:
<!-- T6 · 2026-09-14 11:06 -->
Switching to fortnightly. That halves the load: about two people per day, alternating weeks A and B.

### Zach said:
<!-- T7 · 2026-09-14 11:12 -->
Who should get the reminder text the evening before?

### Claude said:
<!-- T7 · 2026-09-14 11:13 -->
Good question, and it depends on whether you can collect phone numbers. Let me sketch the design first and come back to it.

### Zach said:
<!-- T8 · 2026-09-14 11:20 -->
OK, sketch it.

### Claude said:
<!-- T8 · 2026-09-14 11:22 -->
Design sketch:
- Rota: fortnightly, weeks A and B, about two volunteers per day.
- Each volunteer signs in with their email address to see their slots and tick them off; the sign-in keeps the record trustworthy.
- One admin page for the coordinator to edit the rota.
- Hosting: a free static host plus a small database.
