import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Συλλογή Ελληνικών Τηλεκαρτών", page_icon="📞", layout="wide"
)

CATALOG_FILE = "my_catalog.csv"
IMAGES_DIR = "images"
if not os.path.exists(IMAGES_DIR):
  os.makedirs(IMAGES_DIR)

MONTHS_NUM_LIST = [f"{i:02d}" for i in range(1, 13)] + ["--"]
CONDITION_OPTIONS = ["Άριστη", "Φθαρμένη / Χτυπημένη", "Μέτρια"]
UNITS_OPTIONS = ["100", "200", "500", "1000", "Άλλο"]

MONTH_MAPPING = {
    "Ιανουάριος": "01",
    "Φεβρουάριος": "02",
    "Μάρτιος": "03",
    "Απρίλιος": "04",
    "Μάιος": "05",
    "Ιούνιος": "06",
    "Ιούλιος": "07",
    "Αύγουστος": "08",
    "Σεπτέμβριος": "09",
    "Οκτώβριος": "10",
    "Νοέμβριος": "11",
    "Δεκέμβριος": "12",
}

OFFICIAL_DATA_BY_YEAR = {
    "1992": {"total": 3, "mintage": "50.000"},
    "1993": {"total": 34, "mintage": "50.000"},
    "1994": {"total": 69, "mintage": "50.000"},
    "1995": {"total": 62, "mintage": "50.000"},
    "1996": {"total": 160, "mintage": "50.000"},
    "1997": {"total": 184, "mintage": "50.000"},
    "1998": {"total": 200, "mintage": "50.000"},
    "1999": {"total": 214, "mintage": "50.000"},
    "2000": {"total": 195, "mintage": "50.000"},
    "2001": {"total": 411, "mintage": "50.000"},
    "2002": {"total": 185, "mintage": "50.000"},
    "2003": {"total": 188, "mintage": "50.000"},
    "2004": {"total": 146, "mintage": "50.000"},
    "2005": {"total": 65, "mintage": "50.000"},
    "2006": {"total": 110, "mintage": "50.000"},
    "2007": {"total": 93, "mintage": "50.000"},
    "2008": {"total": 73, "mintage": "50.000"},
    "2009": {"total": 120, "mintage": "50.000"},
    "2010": {"total": 70, "mintage": "50.000"},
    "2011": {"total": 51, "mintage": "50.000"},
    "2012": {"total": 51, "mintage": "50.000"},
    "2013": {"total": 43, "mintage": "50.000"},
    "2014": {"total": 36, "mintage": "50.000"},
    "2015": {"total": 41, "mintage": "50.000"},
    "2016": {"total": 24, "mintage": "50.000"},
    "2017": {"total": 24, "mintage": "50.000"},
    "2018": {"total": 27, "mintage": "50.000"},
    "2019": {"total": 32, "mintage": "50.000"},
    "2020": {"total": 9, "mintage": "50.000"},
    "2021": {"total": 13, "mintage": "50.000"},
    "2022": {"total": 8, "mintage": "50.000"},
    "2023": {"total": 4, "mintage": "50.000"},
    "2024": {"total": 4, "mintage": "50.000"},
    "2025": {"total": 3, "mintage": "50.000"},
}


def convert_year_to_4digits(y):
  y_str = str(y).strip()
  if len(y_str) == 4 and y_str.isdigit():
    return y_str
  if len(y_str) == 2 and y_str.isdigit():
    val = int(y_str)
    if val > 50:
      return "19" + y_str
    else:
      return "20" + y_str
  return y_str


def load_data():
  if os.path.exists(CATALOG_FILE):
    df = pd.read_csv(CATALOG_FILE, dtype=str)

    if "id" in df.columns:
      df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(1).astype(int)
    if "quantity" in df.columns:
      df["quantity"] = (
          pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)
      )

    if "owned" in df.columns:
      df["owned"] = df["owned"].astype(str).str.lower().isin(["true", "1", "yes"])
    else:
      df["owned"] = True

    if "month" in df.columns:
      df["month"] = (
          df["month"]
          .map(lambda m: MONTH_MAPPING.get(m, m if m in MONTHS_NUM_LIST else "--"))
      )
    else:
      df["month"] = "--"

    if "year" in df.columns:
      df["year"] = df["year"].apply(convert_year_to_4digits)
    else:
      df["year"] = "1993"

    if "mintage" not in df.columns:
      df["mintage"] = "Άγνωστο"
    if "condition" not in df.columns:
      df["condition"] = "Άριστη"
    if "category" not in df.columns:
      df["category"] = "Chip"

    df.to_csv(CATALOG_FILE, index=False)
  else:
    df = pd.DataFrame(
        columns=[
            "id",
            "code",
            "title",
            "month",
            "year",
            "units",
            "mintage",
            "category",
            "condition",
            "image_url",
            "back_image_url",
            "owned",
            "quantity",
        ]
    )
    df.to_csv(CATALOG_FILE, index=False)
  return df


df = load_data()

if "last_year" not in st.session_state:
  st.session_state.last_year = "1993"
if "last_month" not in st.session_state:
  st.session_state.last_month = "10"

st.title("📞 Η Συλλογή μου από Ελληνικές Τηλεκάρτες")

st.sidebar.header("📁 Διαχείριση Αρχείου")

csv_data = df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="📥 Κατέβασμα Αρχείου (CSV)",
    data=csv_data,
    file_name="my_catalog.csv",
    mime="text/csv",
)

uploaded_csv = st.sidebar.file_uploader(
    "📤 Φόρτωση Αρχείου (CSV)", type=["csv"]
)

if uploaded_csv is not None:
  try:
    imported_df = pd.read_csv(uploaded_csv, dtype=str)
    imported_df.to_csv(CATALOG_FILE, index=False)
    st.sidebar.success("Το αρχείο φορτώθηκε επιτυχώς!")
    st.rerun()
  except Exception as e:
    st.sidebar.error("Πρόκυψε σφάλμα κατά τη φόρτωση.")

st.sidebar.markdown("---")
st.sidebar.subheader("📋 Εξαγωγή Ζητούμενων (Wishlist)")
if not df.empty:
  wishlist_df = df[df["owned"] == False]
  if not wishlist_df.empty:
    wishlist_csv = wishlist_df[["code", "title", "year", "units"]].to_csv(
        index=False
    ).encode("utf-8")
    st.sidebar.download_button(
        label="📥 Κατέβασμα Λίστας Ελλείψεων",
        data=wishlist_csv,
        file_name="my_wishlist.csv",
        mime="text/csv",
    )
  else:
    st.sidebar.text("Δεν υπάρχουν καταχωρημένες ελλείψεις.")

st.sidebar.markdown("---")
st.sidebar.header("🔍 Αναζήτηση & Φίλτρα")

search_query = st.sidebar.text_input("Αναζήτηση (Κωδικός, Τίτλος)")

available_years = ["Όλα τα έτη"] + sorted(
    list(OFFICIAL_DATA_BY_YEAR.keys()), reverse=True
)
selected_year_filter = st.sidebar.selectbox("📅 Φίλτρο ανά Έτος", available_years)

sort_option = st.sidebar.selectbox(
    "Ταξινόμηση κατά:",
    [
        "Χρονολογική (Παλαιότερες πρώτα)",
        "Χρονολογική (Νεότερες πρώτα)",
        "Αλφαβητικά (Τίτλος A-Ω)",
        "Αλφαβητικά (Κωδικός)",
    ],
)

filter_owned = st.sidebar.checkbox("Εμφάνιση μόνο όσων έχω στη συλλογή")
filter_wishlist = st.sidebar.checkbox("⭐ Εμφάνιση Wishlist (Ζητούμενες)")
filter_damaged = st.sidebar.checkbox(
    "⚠️ Εμφάνιση μόνο Φθαρμένων (για αντικατάσταση)"
)
filter_medium = st.sidebar.checkbox("🟡 Εμφάνιση μόνο Μέτριων")

st.sidebar.markdown("---")
with st.sidebar.expander("📊 Στατιστικά & Γραφήματα Συλλογής", expanded=False):
  owned_df = df[df["owned"] == True] if not df.empty else df
  total_collection_count = len(owned_df)
  total_official_count = sum(
      [info["total"] for info in OFFICIAL_DATA_BY_YEAR.values()]
  )
  total_pct = (
      (total_collection_count / total_official_count * 100)
      if total_official_count > 0
      else 0.0
  )

  st.markdown(
      f"**Γενικό Σύνολο:** `{total_collection_count} / {total_official_count}`"
      f" (**{total_pct:.1f}%**)"
  )
  st.progress(min(1.0, total_pct / 100.0))
  st.markdown("---")

  if not df.empty:
    owned_temp_df = df[df["owned"] == True]
    counts_per_year = owned_temp_df["year"].value_counts()
  else:
    counts_per_year = pd.Series(dtype=int)

  chart_data = []

  for year_str, info in OFFICIAL_DATA_BY_YEAR.items():
    official_total = info["total"]
    user_count = int(counts_per_year.get(year_str, 0))
    yr_pct = (user_count / official_total * 100) if official_total > 0 else 0.0
    chart_data.append({"Έτος": year_str, "Ποσοστό (%)": round(yr_pct, 1)})

    st.text(f"{year_str}: {user_count} / {official_total} ({yr_pct:.1f}%)")
    st.progress(min(1.0, yr_pct / 100.0))

  st.markdown("---")
  st.subheader("📈 Γράφημα Πληρότητας")
  df_chart = pd.DataFrame(chart_data).set_index("Έτος")
  st.bar_chart(df_chart)

st.markdown("---")

# --- ΦΟΡΜΑ ΠΡΟΣΘΗΚΗΣ ΝΕΑΣ ΚΑΡΤΑΣ ---
with st.expander("➕ Προσθήκη Νέας Τηλεκάρτας στη Συλλογή", expanded=False):
  with st.form("add_card_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
      new_code = st.text_input("Κωδικός Κάρτας (π.χ. 95-04)")
      new_title = st.text_input("Τίτλος / Θέμα (π.χ. Φασιανός)")
    with col2:
      c_m, c_y = st.columns(2)
      with c_m:
        m_index = (
            MONTHS_NUM_LIST.index(st.session_state.last_month)
            if st.session_state.last_month in MONTHS_NUM_LIST
            else 9
        )
        new_month = st.selectbox(
            "Μήνας (ΜΜ)", MONTHS_NUM_LIST, index=m_index
        )
      with c_y:
        new_year = st.text_input(
            "Έτος (π.χ. 2000)", value=st.session_state.last_year, max_chars=4
        )
    with col3:
      new_units = st.selectbox("Μονάδες", UNITS_OPTIONS, index=0)

      auto_mintage = OFFICIAL_DATA_BY_YEAR.get(
          convert_year_to_4digits(new_year), {}
      ).get("mintage", "50.000")
      new_mintage = st.text_input("Τιράζ (π.χ. 50.000)", value=auto_mintage)

      new_cat = st.selectbox(
          "Κατηγορία", ["Μαγνητική", "Chip", "Χρονοκάρτα"], index=1
      )
      new_condition = st.selectbox(
          "Κατάσταση Κάρτας", CONDITION_OPTIONS, index=0
      )

    f_col1, f_col2 = st.columns(2)
    with f_col1:
      front_file = st.file_uploader(
          "Μπροστινή Όψη", type=("jpg", "png", "jpeg"), key="add_front"
      )
    with f_col2:
      back_file = st.file_uploader(
          "Πίσω Όψη", type=("jpg", "png", "jpeg"), key="add_back"
      )

    col_a, col_b = st.columns(2)
    with col_a:
      new_owned = st.checkbox("Την έχω στη συλλογή;", value=True)
    with col_b:
      new_qty = st.number_input("Ποσότητα", min_value=1, value=1)

    submit_button = st.form_submit_button("💾 Αποθήκευση Κάρτας")

    if submit_button:
      if not new_code or not new_title:
        st.error("Παρακαλώ συμπλήρωσε τουλάχιστον Κωδικό και Τίτλο!")
      else:
        st.session_state.last_year = convert_year_to_4digits(new_year)
        st.session_state.last_month = str(new_month)

        existing_card = df[
            df["code"].str.strip().str.lower() == new_code.strip().lower()
        ]

        if not existing_card.empty:
          card_id = int(existing_card.iloc[0]["id"])
          current_qty = int(existing_card.iloc[0]["quantity"])
          updated_qty = current_qty + int(new_qty)

          df.loc[df["id"] == card_id, "quantity"] = updated_qty
          df.to_csv(CATALOG_FILE, index=False)
          st.success(
              f"Ο κωδικός '{new_code}' υπάρχει ήδη! Η ποσότητα ενημερώθηκε σε"
              f" {updated_qty}."
          )
          st.rerun()
        else:
          new_id = int(df["id"].max() + 1) if not df.empty else 1

          front_path = "https://via.placeholder.com/200/1e3d59/ffffff?text=Front"
          if front_file is not None:
            os.makedirs(IMAGES_DIR, exist_ok=True)
            ext = front_file.name.split(".")[-1]
            front_filename = f"front_{new_id}.{ext}"
            front_path = os.path.join(IMAGES_DIR, front_filename)
            with open(front_path, "wb") as f:
              f.write(front_file.getbuffer())
            front_path = f"images/{front_filename}"

          back_path = "https://via.placeholder.com/200/cccccc/ffffff?text=Back"
          if back_file is not None:
            os.makedirs(IMAGES_DIR, exist_ok=True)
            ext = back_file.name.split(".")[-1]
            back_filename = f"back_{new_id}.{ext}"
            back_path = os.path.join(IMAGES_DIR, back_filename)
            with open(back_path, "wb") as f:
              f.write(back_file.getbuffer())
            back_path = f"images/{back_filename}"

          new_row = {
              "id": new_id,
              "code": str(new_code),
              "title": str(new_title),
              "month": str(new_month),
              "year": convert_year_to_4digits(new_year),
              "units": str(new_units),
              "mintage": str(new_mintage),
              "category": str(new_cat),
              "condition": str(new_condition),
              "image_url": str(front_path),
              "back_image_url": str(back_path),
              "owned": bool(new_owned),
              "quantity": int(new_qty),
          }

          df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
          df.to_csv(CATALOG_FILE, index=False)
          st.success(f"Η κάρτα '{new_title}' προστέθηκε με επιτυχία!")
          st.rerun()

st.markdown("---")

# --- ΦΙΛΤΡΑΡΙΣΜΑ & ΑΝΑΖΗΤΗΣΗ ---
filtered_df = df.copy()

if selected_year_filter != "Όλα τα έτη":
  filtered_df = filtered_df[filtered_df["year"] == selected_year_filter]

if search_query:
  query = search_query.lower()
  filtered_df = filtered_df[
      filtered_df["code"].str.lower().str.contains(query, na=False)
      | filtered_df["title"].str.lower().str.contains(query, na=False)
  ]

if filter_owned:
  filtered_df = filtered_df[filtered_df["owned"] == True]

if filter_wishlist:
  filtered_df = filtered_df[filtered_df["owned"] == False]

if filter_damaged:
  filtered_df = filtered_df[
      filtered_df["condition"] == "Φθαρμένη / Χτυπημένη"
  ]

if filter_medium:
  filtered_df = filtered_df[filtered_df["condition"] == "Μέτρια"]

if sort_option == "Χρονολογική (Παλαιότερες πρώτα)":
  filtered_df = filtered_df.sort_values(
      by=["year", "month"], ascending=[True, True]
  )
elif sort_option == "Χρονολογική (Νεότερες πρώτα)":
  filtered_df = filtered_df.sort_values(
      by=["year", "month"], ascending=[False, False]
  )
elif sort_option == "Αλφαβητικά (Τίτλος A-Ω)":
  filtered_df = filtered_df.sort_values(by="title", ascending=True)
elif sort_option == "Αλφαβητικά (Κωδικός)":
  filtered_df = filtered_df.sort_values(by="code", ascending=True)

# --- ΣΕΛΙΔΟΠΟΙΗΣΗ (PAGINATION) ---
items_per_page = 24
total_items = len(filtered_df)
total_pages = (
    max(1, (total_items + items_per_page - 1) // items_per_page)
    if total_items > 0
    else 1
)

st.sidebar.markdown("---")
st.sidebar.header("📄 Σελιδοποίηση")
current_page = st.sidebar.number_input(
    "Επιλογή Σελίδας",
    min_value=1,
    max_value=total_pages,
    value=min(1, total_pages),
    step=1,
)
st.sidebar.text(f"Σελίδα {current_page} από {total_pages}")

start_idx = (current_page - 1) * items_per_page
end_idx = start_idx + items_per_page
paginated_df = filtered_df.iloc[start_idx:end_idx]

# --- ΕΜΦΑΝΙΣΗ ΚΑΡΤΩΝ ---
st.subheader(
    f"🖼️ Αποτελέσματα Αναζήτησης / Κάρτες — Σελίδα {current_page} από"
    f" {total_pages} (Σύνολο: {total_items} κάρτες)"
)

if paginated_df.empty:
  st.info(
      "Δεν βρέθηκαν κάρτες που να ταιριάζουν με τα κριτήρια αναζήτησης."
  )
else:
  cols_per_row = 3
  rows = [
      paginated_df.iloc[i : i + cols_per_row]
      for i in range(0, len(paginated_df), cols_per_row)
  ]

  for row_chunk in rows:
    cols = st.columns(cols_per_row)
    for idx, (_, row) in enumerate(row_chunk.iterrows()):
      with cols[idx]:
        front_img = (
            row["image_url"]
            if (
                str(row["image_url"]).startswith("http")
                or os.path.exists(str(row["image_url"]))
            )
            else "https://via.placeholder.com/200/1e3d59/ffffff?text=Front"
        )
        back_img = (
            row["back_image_url"]
            if (
                str(row["back_image_url"]).startswith("http")
                or os.path.exists(str(row["back_image_url"]))
            )
            else "https://via.placeholder.com/200/cccccc/ffffff?text=Back"
        )

        img_c1, img_c2 = st.columns(2)
        with img_c1:
          st.image(front_img, width=130, caption="Μπροστά")
        with img_c2:
          st.image(back_img, width=130, caption="Πίσω")

        cond_str = str(row.get("condition", "Άριστη"))
        if cond_str == "Φθαρμένη / Χτυπημένη":
          badge = " ⚠️ [Φθαρμένη]"
        elif cond_str == "Μέτρια":
          badge = " 🟡 [Μέτρια]"
        else:
          badge = ""

        date_str = f"{row['month']}/{row['year']}"

        st.markdown(f"**{row['code']} - {row['title']}**{badge}")
        st.caption(
            f"📅 **{date_str}** | 🔢 Μονάδες: {row['units']} | Κατάσταση:"
            f" **{cond_str}** | {row['category']}"
        )

        current_owned = bool(row["owned"])
        new_owned = st.checkbox(
            "Την έχω", value=current_owned, key=f"owned_{row['id']}"
        )
        new_qty = st.number_input(
            "Ποσότητα",
            min_value=0,
            value=int(row["quantity"]),
            key=f"qty_{row['id']}",
        )

        if new_owned != current_owned or new_qty != row["quantity"]:
          df.loc[df["id"] == row["id"], "owned"] = new_owned
          df.loc[df["id"] == row["id"], "quantity"] = new_qty
          df.to_csv(CATALOG_FILE, index=False)

        # --- ΕΠΕΞΕΡΓΑΣΙΑ / ΔΙΑΓΡΑΦΗ ΜΕ ΜΟΝΑΔΙΚΑ KEYS ---
        card_id = int(row["id"])
        with st.expander("✏️ Επεξεργασία / Διαγραφή", expanded=False):
          with st.form(f"edit_form_{card_id}"):
            e_code = st.text_input(
                "Κωδικός", value=str(row["code"]), key=f"e_code_{card_id}"
            )
            e_title = st.text_input(
                "Τίτλος", value=str(row["title"]), key=f"e_title_{card_id}"
            )

            em_col, ey_col = st.columns(2)
            with em_col:
              m_str = str(row["month"]).zfill(2)
              m_index = (
                  MONTHS_NUM_LIST.index(m_str)
                  if m_str in MONTHS_NUM_LIST
                  else 12
              )
              e_month = st.selectbox(
                  "Μήνας (ΜΜ)",
                  MONTHS_NUM_LIST,
                  index=m_index,
                  key=f"e_m_{card_id}",
              )

            with ey_col:
              e_year = st.text_input(
                  "Έτος",
                  value=str(row["year"]),
                  max_chars=4,
                  key=f"e_y_{card_id}",
              )

            u_val = str(row["units"])
            u_index = (
                UNITS_OPTIONS.index(u_val) if u_val in UNITS_OPTIONS else 4
            )
            e_units = st.selectbox(
                "Μονάδες",
                UNITS_OPTIONS,
                index=u_index,
                key=f"e_u_{card_id}",
            )

            e_mintage = st.text_input(
                "Τιράζ",
                value=str(row.get("mintage", "Άγνωστο")),
                key=f"e_mint_{card_id}",
            )

            cat_options = ["Μαγνητική", "Chip", "Χρονοκάρτα"]
            c_index = (
                cat_options.index(row["category"])
                if row["category"] in cat_options
                else 1
            )
            e_cat = st.selectbox(
                "Κατηγορία",
                cat_options,
                index=c_index,
                key=f"e_c_{card_id}",
            )

            cond_idx = (
                CONDITION_OPTIONS.index(cond_str)
                if cond_str in CONDITION_OPTIONS
                else 0
            )
            e_cond = st.selectbox(
                "Κατάσταση Κάρτας",
                CONDITION_OPTIONS,
                index=cond_idx,
                key=f"e_cond_{card_id}",
            )

            e_front = st.file_uploader(
                "Νέα Μπροστινή Όψη",
                type=("jpg", "png", "jpeg"),
                key=f"e_ef_{card_id}",
            )
            e_back = st.file_uploader(
                "Νέα Πίσω Όψη",
                type=("jpg", "png", "jpeg"),
                key=f"e_eb_{card_id}",
            )

            col_save, col_del = st.columns(2)
            with col_save:
              save_edit = st.form_submit_button(
                  "💾 Αποθήκευση", key=f"save_btn_{card_id}"
              )
            with col_del:
              delete_card = st.form_submit_button(
                  "🗑️ Διαγραφή", key=f"del_btn_{card_id}"
              )

            if save_edit:
              df.loc[df["id"] == card_id, "code"] = str(e_code)
              df.loc[df["id"] == card_id, "title"] = str(e_title)
              df.loc[df["id"] == card_id, "month"] = str(e_month)
              df.loc[df["id"] == card_id, "year"] = convert_year_to_4digits(
                  e_year
              )
              df.loc[df["id"] == card_id, "units"] = str(e_units)
              df.loc[df["id"] == card_id, "mintage"] = str(e_mintage)
              df.loc[df["id"] == card_id, "category"] = str(e_cat)
              df.loc[df["id"] == card_id, "condition"] = str(e_cond)

              if e_front is not None:
                ext = e_front.name.split(".")[-1]
                front_filename = f"front_{card_id}.{ext}"
                front_path = os.path.join(IMAGES_DIR, front_filename)
                os.makedirs(IMAGES_DIR, exist_ok=True)
                with open(front_path, "wb") as f:
                  f.write(e_front.getbuffer())
                df.loc[df["id"] == card_id, "image_url"] = (
                    f"images/{front_filename}"
                )

              if e_back is not None:
                ext = e_back.name.split(".")[-1]
                back_filename = f"back_{card_id}.{ext}"
                back_path = os.path.join(IMAGES_DIR, back_filename)
                os.makedirs(IMAGES_DIR, exist_ok=True)
                with open(back_path, "wb") as f:
                  f.write(e_back.getbuffer())
                df.loc[df["id"] == card_id, "back_image_url"] = (
                    f"images/{back_filename}"
                )

              df.to_csv(CATALOG_FILE, index=False)
              st.success("Οι αλλαγές αποθηκεύτηκαν!")
              st.rerun()

            if delete_card:
              df = df[df["id"] != card_id]
              df.to_csv(CATALOG_FILE, index=False)
              st.success("Η κάρτα διαγράφηκε!")
              st.rerun()

        st.markdown("---")