# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: user-data-router.spec.js >> favorites router >> one user cannot read or delete another user's records
- Location: tests\e2e\user-data-router.spec.js:90:5

# Error details

```
Error: expect(received).toBeTruthy()

Received: false
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | 
  3   | // Exercises backend/app/routers/user_data.py end to end over real HTTP
  4   | // (no mocking) to confirm the shared list/delete/clear helpers behave
  5   | // identically to the pre-refactor per-resource implementations, for both
  6   | // the history and favorites resources, and don't leak data across users.
  7   | 
  8   | function uniqueEmail(label) {
  9   |   return `${label}-${Date.now()}-${Math.floor(Math.random() * 1e6)}@example.com`;
  10  | }
  11  | 
  12  | async function signup(request, email) {
  13  |   const res = await request.post('/auth/signup', {
  14  |     data: { email, password: 'securepassword123' },
  15  |   });
> 16  |   expect(res.ok()).toBeTruthy();
      |                    ^ Error: expect(received).toBeTruthy()
  17  |   const body = await res.json();
  18  |   return { token: body.access_token, headers: { Authorization: `Bearer ${body.access_token}` } };
  19  | }
  20  | 
  21  | for (const resource of [
  22  |   {
  23  |     name: 'history',
  24  |     listPath: '/user/history',
  25  |     itemPath: (id) => `/user/history/${id}`,
  26  |     payload: () => ({
  27  |       action: 'analyze',
  28  |       code: 'def hello(): pass',
  29  |       result_json: '{"status": "ok"}',
  30  |     }),
  31  |     notFoundDetail: 'History record not found',
  32  |   },
  33  |   {
  34  |     name: 'favorites',
  35  |     listPath: '/user/favorites',
  36  |     itemPath: (id) => `/user/favorites/${id}`,
  37  |     payload: () => ({
  38  |       title: 'My snippet',
  39  |       action: 'analyze',
  40  |       code: 'def hello(): pass',
  41  |       result_json: '{"status": "ok"}',
  42  |     }),
  43  |     notFoundDetail: 'Favorite not found',
  44  |   },
  45  | ]) {
  46  |   test.describe(`${resource.name} router`, () => {
  47  |     test(`create, list (paginated), delete-one and clear-all round trip`, async ({ request }) => {
  48  |       const { headers } = await signup(request, uniqueEmail(`user-${resource.name}`));
  49  | 
  50  |       const ids = [];
  51  |       for (let i = 0; i < 3; i++) {
  52  |         const res = await request.post(resource.listPath, { headers, data: resource.payload() });
  53  |         expect(res.status()).toBe(200);
  54  |         ids.push((await res.json()).id);
  55  |       }
  56  | 
  57  |       // Pagination: limit=2 should return only the 2 most recent records.
  58  |       const paged = await request.get(`${resource.listPath}?limit=2&offset=0`, { headers });
  59  |       expect(paged.ok()).toBeTruthy();
  60  |       const pagedBody = await paged.json();
  61  |       expect(pagedBody).toHaveLength(2);
  62  |       expect(pagedBody[0].id).toBe(ids[2]);
  63  |       expect(pagedBody[1].id).toBe(ids[1]);
  64  | 
  65  |       const full = await request.get(resource.listPath, { headers });
  66  |       expect((await full.json())).toHaveLength(3);
  67  | 
  68  |       // Delete one record, then confirm it's gone and the rest remain.
  69  |       const del = await request.delete(resource.itemPath(ids[0]), { headers });
  70  |       expect(del.status()).toBe(200);
  71  | 
  72  |       const afterDelete = await request.get(resource.listPath, { headers });
  73  |       const remainingIds = (await afterDelete.json()).map((r) => r.id);
  74  |       expect(remainingIds.sort()).toEqual([ids[1], ids[2]].sort());
  75  | 
  76  |       // Deleting the same record again must 404 with the resource's own message.
  77  |       const redelete = await request.delete(resource.itemPath(ids[0]), { headers });
  78  |       expect(redelete.status()).toBe(404);
  79  |       expect((await redelete.json()).detail).toBe(resource.notFoundDetail);
  80  | 
  81  |       // Clear-all reports the correct remaining count and empties the list.
  82  |       const clear = await request.delete(resource.listPath, { headers });
  83  |       expect(clear.status()).toBe(200);
  84  |       expect((await clear.json()).deleted).toBe(2);
  85  | 
  86  |       const afterClear = await request.get(resource.listPath, { headers });
  87  |       expect(await afterClear.json()).toEqual([]);
  88  |     });
  89  | 
  90  |     test('one user cannot read or delete another user\'s records', async ({ request }) => {
  91  |       const owner = await signup(request, uniqueEmail(`owner-${resource.name}`));
  92  |       const intruder = await signup(request, uniqueEmail(`intruder-${resource.name}`));
  93  | 
  94  |       const create = await request.post(resource.listPath, {
  95  |         headers: owner.headers,
  96  |         data: resource.payload(),
  97  |       });
  98  |       const ownedId = (await create.json()).id;
  99  | 
  100 |       // The intruder's own list must not include the owner's record.
  101 |       const intruderList = await request.get(resource.listPath, { headers: intruder.headers });
  102 |       expect((await intruderList.json()).map((r) => r.id)).not.toContain(ownedId);
  103 | 
  104 |       // Deleting by ID cross-user must 404, not succeed or leak existence.
  105 |       const crossDelete = await request.delete(resource.itemPath(ownedId), {
  106 |         headers: intruder.headers,
  107 |       });
  108 |       expect(crossDelete.status()).toBe(404);
  109 | 
  110 |       // The record must still exist for its real owner afterwards.
  111 |       const ownerList = await request.get(resource.listPath, { headers: owner.headers });
  112 |       expect((await ownerList.json()).map((r) => r.id)).toContain(ownedId);
  113 |     });
  114 | 
  115 |     test('requires authentication', async ({ request }) => {
  116 |       const res = await request.get(resource.listPath);
```