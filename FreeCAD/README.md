# FreeCAD Utilities
### Plan
- [ ] Add new part macro
    - Create revision table spreadsheet
    - Remove draft watermark
- [ ] Add drawing page macro 
    - Use reduced title block after the first page
    - Add full revision table to new pages and partial to pages after
- [ ] Export part button (Export part as step, drawing as pdf and place together)
    - Set sheet scale, description, weight, material, finish, coating
    - Run the drawing verification macro
    - Update ensure revision is reviewed in revision table or add Draft watermark
    - After export setup new revision
- [ ] Drawing verification macro
    - Relabel views
    - Check view sizes againds sheet size
    - Check for True dimensions without true text
    - Check material, finish, and coating are set and compatible
    - Save overrides into objects
