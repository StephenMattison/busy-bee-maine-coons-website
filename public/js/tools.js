/* Busy Bee Maine Coons — interactive tool calculators
   All math runs client-side. No tracking. */

(function () {
  'use strict';

  function show(id, html) {
    var el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = html;
    el.hidden = false;
    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // ============ ADULT SIZE PREDICTOR ============
  // Maine Coon growth model: kittens reach ~75% adult weight by 12 mo,
  // ~95% by 36 mo. Average adult: M 15–25 lb, F 8–12 lb.
  window.predictSize = function () {
    var w = parseFloat(document.getElementById('size-weight').value);
    var a = parseFloat(document.getElementById('size-age').value);
    var sex = document.getElementById('size-sex').value;
    if (!w || !a) { show('size-result', '<p>Please enter weight and age.</p>'); return; }

    // Approx % of adult weight reached at age (months)
    var pctTable = [
      [1, 0.06], [2, 0.12], [3, 0.18], [4, 0.24], [5, 0.30],
      [6, 0.36], [8, 0.46], [10, 0.55], [12, 0.62],
      [18, 0.78], [24, 0.88], [36, 0.96], [48, 1.0], [60, 1.0]
    ];
    var pct = 1.0;
    for (var i = 0; i < pctTable.length; i++) {
      if (a <= pctTable[i][0]) {
        if (i === 0) { pct = pctTable[0][1]; break; }
        var p1 = pctTable[i - 1], p2 = pctTable[i];
        pct = p1[1] + (p2[1] - p1[1]) * ((a - p1[0]) / (p2[0] - p1[0]));
        break;
      }
    }
    var projected = w / pct;
    // Sanity-clamp to breed range
    var min = sex === 'male' ? 13 : 8;
    var max = sex === 'male' ? 26 : 14;
    var low = Math.max(min, projected * 0.9);
    var high = Math.min(max, projected * 1.1);
    var typicalRange = sex === 'male' ? '15–25 lb' : '8–12 lb';

    show('size-result',
      '<h3>Projected adult weight</h3>' +
      '<p class="big-number">' + low.toFixed(1) + ' – ' + high.toFixed(1) + ' lbs</p>' +
      '<p>At ' + a + ' months your kitten is ~' + Math.round(pct * 100) + '% of adult size. ' +
      'Typical adult ' + sex + ' Maine Coon: <strong>' + typicalRange + '</strong>.</p>' +
      '<p class="muted">Genetics, neuter age, and nutrition all affect final size. Maine Coons keep filling out until 3–5 years old.</p>'
    );
  };

  // ============ LIFETIME COST CALCULATOR ============
  window.calcCost = function () {
    var food = +document.getElementById('cost-food').value;
    var litter = +document.getElementById('cost-litter').value;
    var ins = +document.getElementById('cost-insurance').value;
    var vet = +document.getElementById('cost-vet').value;
    var years = Math.max(1, +document.getElementById('cost-years').value || 15);

    var monthly = food + litter + ins;
    var annual = monthly * 12 + vet;
    var setupCost = 850; // bed, tower, carrier, bowls, initial vet
    var year1 = annual + setupCost;
    var lifetime = setupCost + annual * years;

    var fmt = function (n) { return '$' + n.toLocaleString('en-US', { maximumFractionDigits: 0 }); };

    show('cost-result',
      '<h3>Your estimate</h3>' +
      '<table class="tool-table">' +
      '<tr><td>One-time setup</td><td>' + fmt(setupCost) + '</td></tr>' +
      '<tr><td>Monthly recurring</td><td>' + fmt(monthly) + '</td></tr>' +
      '<tr><td>Annual (incl. vet)</td><td>' + fmt(annual) + '</td></tr>' +
      '<tr class="emph"><td>Year 1 total</td><td>' + fmt(year1) + '</td></tr>' +
      '<tr class="emph"><td>' + years + '-year lifetime</td><td>' + fmt(lifetime) + '</td></tr>' +
      '</table>' +
      '<p class="muted">Excludes adoption fee, emergencies, and boarding. Use as a planning floor, not a ceiling.</p>'
    );
  };

  // ============ GROOMING PLANNER ============
  window.planGrooming = function () {
    var coat = document.getElementById('groom-coat').value;
    var life = document.getElementById('groom-life').value;
    var season = document.getElementById('groom-season').value;

    var brush = 2; // baseline times/week
    if (coat === 'medium') brush = 3;
    if (coat === 'heavy') brush = 5;
    if (life === 'mixed') brush += 1;
    if (life === 'outdoor') brush += 2;
    if (season === 'yes') brush = Math.min(7, brush + 2);

    var bath = coat === 'heavy' ? 'every 4–6 weeks' : 'every 6–8 weeks';
    if (life === 'outdoor') bath = 'every 3–4 weeks';

    var tools = [
      'Wide-tooth steel comb (essential)',
      'Slicker brush for undercoat',
      'Stainless dematting comb',
      'Pet-safe shampoo &amp; blow dryer (low heat)'
    ];

    show('groom-result',
      '<h3>Your grooming schedule</h3>' +
      '<ul class="tool-list">' +
      '<li><strong>Brushing:</strong> ' + brush + '× per week (' + (brush >= 7 ? 'daily' : '~' + Math.round(7 / brush) + ' day intervals') + ')</li>' +
      '<li><strong>Bath:</strong> ' + bath + '</li>' +
      '<li><strong>Nail trim:</strong> every 2–3 weeks</li>' +
      '<li><strong>Ear check:</strong> weekly</li>' +
      '<li><strong>Dental:</strong> brush 2–3×/week, vet cleaning yearly</li>' +
      '</ul>' +
      '<h4>Recommended tools</h4>' +
      '<ul class="tool-list">' + tools.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul>' +
      '<p class="muted">Maine Coons love water — start bath training young and most will tolerate (or enjoy) it for life.</p>'
    );
  };

  // ============ COMPATIBILITY QUIZ ============
  window.scoreQuiz = function () {
    var ids = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6'];
    var total = 0;
    for (var i = 0; i < ids.length; i++) total += +document.getElementById(ids[i]).value;
    var max = ids.length * 3;
    var pct = Math.round((total / max) * 100);

    var verdict, body;
    if (pct >= 80) {
      verdict = 'Excellent match 🎉';
      body = 'You have the time, space, and budget a Maine Coon thrives on. This breed will fit beautifully into your life.';
    } else if (pct >= 60) {
      verdict = 'Strong match';
      body = 'You\'re well-prepared. Address the lower-scoring areas (more daily interaction, grooming routine, or budget cushion) and you\'re set.';
    } else if (pct >= 40) {
      verdict = 'Possible — with planning';
      body = 'A Maine Coon is doable but you\'ll want to adjust schedule, space, or budget first. Consider an older rescue or a calmer breed.';
    } else {
      verdict = 'Not the right time';
      body = 'Maine Coons demand commitment. A lower-maintenance breed or waiting until your situation changes will be kinder to both of you.';
    }

    show('quiz-result',
      '<h3>' + verdict + '</h3>' +
      '<p class="big-number">' + pct + '%</p>' +
      '<p>' + body + '</p>' +
      '<p><a href="/contact" class="btn btn-outline">Talk to a breeder</a></p>'
    );
  };

  // ============ NAME GENERATOR ============
  var NAMES = {
    regal: {
      male: ['Aragorn', 'Augustus', 'Caesar', 'Maximus', 'Cyrus', 'Magnus', 'Octavian', 'Lancelot', 'Theodore', 'Atticus', 'Sterling', 'Wellington', 'Beauregard', 'Reginald', 'Sebastian', 'Cassius', 'Leopold', 'Bartholomew'],
      female: ['Athena', 'Cleopatra', 'Seraphina', 'Isadora', 'Anastasia', 'Genevieve', 'Persephone', 'Octavia', 'Cordelia', 'Calliope', 'Esmeralda', 'Wilhelmina', 'Evangeline', 'Penelope', 'Beatrice', 'Magnolia']
    },
    nature: {
      male: ['Bear', 'Wolf', 'Fox', 'Hawk', 'Cedar', 'Birch', 'Storm', 'River', 'Ranger', 'Forest', 'Granite', 'Hunter', 'Maple', 'Timber', 'Boulder', 'Hawk', 'Loki', 'Thor'],
      female: ['Willow', 'Luna', 'Aurora', 'Nova', 'Sage', 'Hazel', 'Juniper', 'Iris', 'Fern', 'Rain', 'Misty', 'Aspen', 'Daisy', 'Ivy', 'Wren', 'Freya', 'Selene']
    },
    playful: {
      male: ['Biscuit', 'Pickle', 'Waffles', 'Mochi', 'Pumpkin', 'Cookie', 'Bingo', 'Scout', 'Buddy', 'Tater', 'Noodle', 'Gizmo', 'Pippin', 'Otis', 'Murphy', 'Finn', 'Milo'],
      female: ['Muffin', 'Honey', 'Peaches', 'Cupcake', 'Pixie', 'Coco', 'Daisy', 'Lulu', 'Mochi', 'Pearl', 'Poppy', 'Bean', 'Clover', 'Olive', 'Penny', 'Ruby']
    },
    classic: {
      male: ['Maine', 'Bangor', 'Acadia', 'Atlas', 'Captain', 'Skipper', 'Mariner', 'Hudson', 'Lincoln', 'Henley', 'Holden', 'Kennedy', 'Sawyer'],
      female: ['Augusta', 'Portland', 'Acadia', 'Liberty', 'Harbor', 'Bay', 'Marina', 'Holly', 'Caroline', 'Eleanor', 'Madison', 'Charlotte']
    }
  };
  window.generateName = function () {
    var style = document.getElementById('name-style').value;
    var sex = document.getElementById('name-sex').value;
    var styles = style === 'any' ? Object.keys(NAMES) : [style];
    var sexes = sex === 'any' ? ['male', 'female'] : [sex];

    var pool = [];
    styles.forEach(function (s) {
      sexes.forEach(function (x) {
        pool = pool.concat(NAMES[s][x]);
      });
    });
    // Dedupe
    pool = pool.filter(function (n, i) { return pool.indexOf(n) === i; });
    // Shuffle, take 5
    for (var i = pool.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = pool[i]; pool[i] = pool[j]; pool[j] = t;
    }
    var picks = pool.slice(0, 5);

    show('name-result',
      '<h3>Your name ideas</h3>' +
      '<ul class="tool-list name-list">' + picks.map(function (n) { return '<li>' + n + '</li>'; }).join('') + '</ul>' +
      '<p><button type="button" class="btn btn-outline" onclick="generateName()">Generate 5 more</button></p>'
    );
  };

  // ============ DAILY FEEDING CALCULATOR ============
  // RER = 70 × weight(kg)^0.75. MER = RER × multiplier
  window.calcFeeding = function () {
    var lbs = parseFloat(document.getElementById('feed-weight').value);
    if (!lbs) { show('feed-result', '<p>Please enter your cat\'s weight.</p>'); return; }
    var kg = lbs / 2.2046;
    var stage = document.getElementById('feed-stage').value;
    var body = document.getElementById('feed-body').value;
    var act = document.getElementById('feed-activity').value;

    var rer = 70 * Math.pow(kg, 0.75);
    var mult = 1.2; // neutered adult baseline
    if (stage === 'kitten') mult = 2.5;
    else if (stage === 'young') mult = 1.4;
    else if (stage === 'senior') mult = 1.1;

    if (body === 'over') mult *= 0.8;
    if (body === 'under') mult *= 1.2;
    if (act === 'high') mult *= 1.15;
    if (act === 'low') mult *= 0.9;

    var kcal = Math.round(rer * mult);
    // Typical premium dry: ~400 kcal/cup. Wet 5.5oz can: ~180 kcal.
    var cups = (kcal / 400);
    var cans = (kcal / 180);

    show('feed-result',
      '<h3>Daily target</h3>' +
      '<p class="big-number">' + kcal + ' kcal/day</p>' +
      '<table class="tool-table">' +
      '<tr><td>If feeding dry only</td><td>~' + cups.toFixed(2) + ' cups (≈400 kcal/cup)</td></tr>' +
      '<tr><td>If feeding wet only</td><td>~' + cans.toFixed(1) + ' × 5.5oz cans</td></tr>' +
      '<tr><td>50/50 split</td><td>~' + (cups / 2).toFixed(2) + ' cup dry + ' + (cans / 2).toFixed(1) + ' cans wet</td></tr>' +
      '</table>' +
      '<p class="muted">Always check the kcal/cup on your specific food bag — values vary widely. Adjust by ±10% based on monthly weight checks. Consult your vet for medical conditions.</p>'
    );
  };
})();
