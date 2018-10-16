-- description:Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item.
PRAGMA foreign_keys = ON;
drop trigger if exists trigger14_add;
create trigger trigger14_add
before insert on Bids
for each row
when exists (
        Select * 
        from items
        where new.amount > items.Currently and Items.ItemID = new.ItemID
    )
begin
  select raise(rollback, 'Any new bid must have a higher amount than any of the previous bides.');
end;