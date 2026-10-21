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

MONTHS_LIST = [
    "Ιανουάριος",
    "Φεβρουάριος",
    "Μάρτιος",
    "Απρίλιος",
    "Μάιος",
    "Ιούνιος",
    "Ιούλιος",
    "Αύγουστος",
    "Σεπτέμβριος",
    "Οκτώβριος",
    "Νοέμβριος",
    "Δεκέμβριος",
    "Άγνωστος / Δεν αναγράφεται",
]

CONDITION_OPTIONS = ["Άριστη", "Φθαρμένη / Χτυπημένη", "Μέτρια"]


def load_data():
  if os.path.exists(CATALOG_FILE):
    df = pd.read_csv(CATALOG_FILE)
    df["units"] = df["units"].astype(str)
    if "month" not in df.columns:
      df["month"] = "Άγνωστος / Δεν αναγράφεται"
    if "mintage" not in df.columns:
      df["mintage"] = "Άγνωστο"
    if "back_image_url" not in df.columns:
      df["back_image_url"] = (
          "https://via.placeholder.com/200/cccccc/ffffff?text=No+Back"
      )
    if "condition" not in df.columns:
      df["condition"] = "Άριστη"
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

st.title("📞 Η Συλλογή μου από Ελληνικές Τηλεκάρτες")

# --- ΔΙΑΧΕΙΡΙΣΗ ΑΡΧΕΙΟΥ & ΑΝΑΖΗΤΗΣΗ / ΦΙΛΤΡΑ ΣΤΟ SIDEBAR ---
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
    imported_df = pd.read_csv(uploaded_csv)
    imported_df["units"] = imported_df["units"].astype(str)
    imported_df.to_csv(CATALOG_FILE, index=False)
    st.sidebar.success("Το αρχείο φορτώθηκε επιτυχώς!")
    st.rerun()
  except Exception as e:
    st.sidebar.error("Πρόκυψε σφάλμα κατά τη φόρτωση.")

st.sidebar.markdown("---")
st.sidebar.header("🔍 Αναζήτηση & Ταξινόμηση")

# Πεδίο Αναζήτησης
search_query = st.sidebar.text_input("Αναζήτηση (Κωδικός ή Τίτλος)")

# Επιλογή Ταξινόμησης
sort_option = st.sidebar.selectbox(
    "Ταξινόμηση κατά:",
    [
        "Χρονολογική (Παλαιότερες πρώτα)",
        "Χρονολογική (Νεότερες πρώτα)",
        "Αλφαβητικά (Τίτλος A-Ω)",
        "Αλφαβητικά (Κωδικός)",
    ],
)

# Φίλτρα εμφάνισης
filter_owned = st.sidebar.checkbox("Εμφάνιση μόνο όσων έχω στη συλλογή")
filter_damaged = st.sidebar.checkbox(
    "⚠️ Εμφάνιση μόνο Φθαρμένων (για αντικατάσταση)"
)

st.markdown("---")

# --- ΦΟΡΜΑ ΠΡΟΣΘΗΚΗΣ ΝΕΑΣ ΚΑΡΤΑΣ ---
with st.expander("➕ Προσθήκη Νέας Τηλεκάρτας στη Συλλογή", expanded=False):
  with st.form("add_card_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
      new_code = st.text_input("Κωδικός Κάρτας (π.χ. 95-04)")
      new_title = st.text_input("Τίτλος / Θέμα (π.χ. Φασιανός)")
    with col2:
      new_month = st.selectbox("Μήνας Κυκλοφορίας", MONTHS_LIST)
      new_year = st.number_input(
          "Έτος Κυκλοφορίας", min_value=1990, max_value=2030, value=1995
      )
    with col3:
      new_units = st.selectbox(
          "Μονάδες", ["100", "500", "1000", "Άλλο"], index=0
      )
      new_mintage = st.text_input("Τιράζ (π.χ. 50.000)", value="Άγνωστο")
      new_cat = st.selectbox("Κατηγορία", ["Μαγνητικές", "Chip", "Χρονοκάρτα"])
      new_condition = st.selectbox(
          "Κατάσταση Κάρτας", CONDITION_OPTIONS, index=0
      )

    f_col1, f_col2 = st.columns(2)
    with f_col1:
      front_file = st.file_uploader(
          "Μπροστινή Όψη", type=["jpg", "png", "jpeg"], key="add_front"
      )
    with f_col2:
      back_file = st.file_uploader(
          "Πίσω Όψη", type=["jpg", "png", "jpeg"], key="add_back"
      )

    col_a, col_b = st.columns(2)
    with col_a:
      new_owned = st.checkbox("Την έχω στη συλλογή;", value=True)
    with col_b:
      new_qty = st.number_input("Ποσότητα", min_value=0, value=1)

    submit_button = st.form_submit_button("💾 Αποθήκευση Κάρτας")

    if submit_button:
      if not new_code or not new_title:
        st.error("Παρακαλώ συμπλήρωσε τουλάχιστον Κωδικό και Τίτλο!")
      else:
        front_path = (
            "https://via.placeholder.com/200/1e3d59/ffffff?text=Front"
        )
        if front_file is not None:
          front_path = os.path.join(IMAGES_DIR, "front_" + front_file.name)
          with open(front_path, "wb") as f:
            f.write(front_file.getbuffer())

        back_path = "https://via.placeholder.com/200/cccccc/ffffff?text=Back"
        if back_file is not None:
          back_path = os.path.join(IMAGES_DIR, "back_" + back_file.name)
          with open(back_path, "wb") as f:
            f.write(back_file.getbuffer())

        new_id = int(df["id"].max() + 1) if not df.empty else 1

        new_row = {
            "id": new_id,
            "code": new_code,
            "title": new_title,
            "month": new_month,
            "year": int(new_year),
            "units": str(new_units),
            "mintage": str(new_mintage),
            "category": new_cat,
            "condition": new_condition,
            "image_url": front_path,
            "back_image_url": back_path,
            "owned": new_owned,
            "quantity": int(new_qty),
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df["units"] = df["units"].astype(str)
        df.to_csv(CATALOG_FILE, index=False)
        st.success(f"Η κάρτα '{new_title}' προστέθηκε με επιτυχία!")
        st.rerun()

st.markdown("---")

# --- ΕΦΑΡΜΟΓΗ ΦΙΛΤΡΩΝ & ΤΑΞΙΝΟΜΗΣΗΣ ---
filtered_df = df.copy()

if search_query:
  query = search_query.lower()
  filtered_df = filtered_df[
      filtered_df["code"].str.lower().str.contains(query, na=False)
      | filtered_df["title"].str.lower().str.contains(query, na=False)
  ]

if filter_owned:
  filtered_df = filtered_df[filtered_df["owned"] == True]

if filter_damaged:
  filtered_df = filtered_df[
      filtered_df["condition"] == "Φθαρμένη / Χτυπημένη"
  ]

if sort_option == "Χρονολογική (Παλαιότερες πρώτα)":
  filtered_df = filtered_df.sort_values(by="year", ascending=True)
elif sort_option == "Χρονολογική (Νεότερες πρώτα)":
  filtered_df = filtered_df.sort_values(by="year", ascending=False)
elif sort_option == "Αλφαβητικά (Τίτλος A-Ω)":
  filtered_df = filtered_df.sort_values(by="title", ascending=True)
elif sort_option == "Αλφαβητικά (Κωδικός)":
  filtered_df = filtered_df.sort_values(by="code", ascending=True)

# --- ΕΜΦΑΝΙΣΗ ΚΑΡΤΩΝ ---
st.subheader("🖼️ Οι Κάρτες σου")

if filtered_df.empty:
  st.info(
      "Δεν βρέθηκαν κάρτες που να ταιριάζουν με τα κριτήρια αναζήτησης."
  )
else:
  cols_per_row = 3
  rows = [
      filtered_df.iloc[i : i + cols_per_row]
      for i in range(0, len(filtered_df), cols_per_row)
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

        # Επισήμανση αν είναι φθαρμένη
        cond_str = str(row.get("condition", "Άριστη"))
        badge = " ⚠️ [Φθαρμένη]" if cond_str == "Φθαρμένη / Χτυπημένη" else ""

        st.markdown(f"**{row['code']} - {row['title']}**{badge}")
        st.caption(
            f"📅 {row['month']} {row['year']} | 🔢 Μονάδες: {row['units']} |"
            f" Κατάσταση: **{cond_str}**"
        )

        current_owned = row["owned"]
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
          df["units"] = df["units"].astype(str)
          df.to_csv(CATALOG_FILE, index=False)

        # --- ΕΠΕΞΕΡΓΑΣΙΑ / ΔΙΑΓΡΑΦΗ ---
        with st.expander("✏️ Επεξεργασία / Διαγραφή", expanded=False):
          with st.form(f"edit_form_{row['id']}"):
            e_code = st.text_input("Κωδικός", value=str(row["code"]))
            e_title = st.text_input("Τίτλος", value=str(row["title"]))

            m_index = (
                MONTHS_LIST.index(row["month"])
                if row["month"] in MONTHS_LIST
                else 12
            )
            e_month = st.selectbox(
                "Μήνας", MONTHS_LIST, index=m_index, key=f"m_{row['id']}"
            )

            e_year = st.number_input(
                "Έτος",
                min_value=1990,
                max_value=2030,
                value=int(row["year"]),
                key=f"y_{row['id']}",
            )

            units_options = ["100", "500", "1000", "Άλλο"]
            u_val = str(row["units"])
            u_index = (
                units_options.index(u_val) if u_val in units_options else 3
            )
            e_units = st.selectbox(
                "Μονάδες", units_options, index=u_index, key=f"u_{row['id']}"
            )

            e_mintage = st.text_input(
                "Τιράζ",
                value=str(row.get("mintage", "Άγνωστο")),
                key=f"mint_{row['id']}",
            )

            cat_options = ["Μαγνητικές", "Chip", "Χρονοκάρτα"]
            c_index = (
                cat_options.index(row["category"])
                if row["category"] in cat_options
                else 0
            )
            e_cat = st.selectbox(
                "Κατηγορία", cat_options, index=c_index, key=f"c_{row['id']}"
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
                key=f"cond_{row['id']}",
            )

            e_front = st.file_uploader(
                "Νέα Μπροστινή Όψη",
                type=["jpg", "png", "jpeg"],
                key=f"ef_{row['id']}",
            )
            e_back = st.file_uploader(
                "Νέα Πίσω Όψη",
                type=["jpg", "png", "jpeg"],
                key=f"eb_{row['id']}",
            )

            col_save, col_del = st.columns(2)
            with col_save:
              save_edit = st.form_submit_button("💾 Αποθήκευση")
            with col_del:
              delete_card = st.form_submit_button("🗑️ Διαγραφή")

            if save_edit:
              df.loc[df["id"] == row["id"], "code"] = e_code
              df.loc[df["id"] == row["id"], "title"] = e_title
              df.loc[df["id"] == row["id"], "month"] = e_month
              df.loc[df["id"] == row["id"], "year"] = int(e_year)
              df.loc[df["id"] == row["id"], "units"] = str(e_units)
              df.loc[df["id"] == row["id"], "mintage"] = str(e_mintage)
              df.loc[df["id"] == row["id"], "category"] = e_cat
              df.loc[df["id"] == row["id"], "condition"] = e_cond

              if e_front is not None:
                front_path = os.path.join(IMAGES_DIR, "front_" + e_front.name)
                with open(front_path, "wb") as f:
                  f.write(e_front.getbuffer())
                df.loc[df["id"] == row["id"], "image_url"] = front_path

              if e_back is not None:
                back_path = os.path.join(IMAGES_DIR, "back_" + e_back.name)
                with open(back_path, "wb") as f:
                  f.write(e_back.getbuffer())
                df.loc[df["id"] == row["id"], "back_image_url"] = back_path

              df["units"] = df["units"].astype(str)
              df.to_csv(CATALOG_FILE, index=False)
              st.success("Οι αλλαγές αποθηκεύτηκαν!")
              st.rerun()

            if delete_card:
              df = df[df["id"] != row["id"]]
              df["units"] = df["units"].astype(str)
              df.to_csv(CATALOG_FILE, index=False)
              st.success("Η κάρτα διαγράφηκε!")
              st.rerun()

        st.markdown("---")